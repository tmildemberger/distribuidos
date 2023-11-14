import grpc
import gestor_de_estoque_pb2
import gestor_de_estoque_pb2_grpc

from flask import Flask
from flask_sse import sse

from concurrent import futures
import threading
import time
from datetime import datetime, timedelta

import flask.cli
flask.cli.show_server_banner = lambda *args: None

import logging
logging.getLogger("werkzeug").setLevel(logging.ERROR)

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

class GestorDeEstoqueServicer(gestor_de_estoque_pb2_grpc.GestorDeEstoqueServicer):
    """Classe que implementa todas as RPCs do arquivo .proto."""
    
    def __init__(self, minutos):
        # variáveis para controle do estoque em si
        self.produtos_cadastrados = dict()
        self.estoque = dict()
        self.historico = dict()
        self.sse_url = ''
        self.minutos = minutos

    def checaNotificacaoSemSaida(self):
        while True:
            agora = datetime.now()
            delta = timedelta(minutes=self.minutos)
            
            inicio_periodo = (agora-delta).isoformat()
            fim_periodo = agora.isoformat()
            
            sem_saida = []
            com_saida = set()
            for (momento, movimentacao) in self.historico.items():
                if momento > inicio_periodo and momento < fim_periodo:
                    if movimentacao.tipo == "Saída":
                        com_saida.add(movimentacao.codigo)
            
            sem_estoque = set()
            for (codigo, quantidade) in self.estoque.items():
                if quantidade == 0:
                    sem_estoque.add(codigo)
            
            sem_saida = set(self.produtos_cadastrados.keys()) - com_saida - sem_estoque

            if len(sem_saida) > 0:
                # vai mandar notificação
                with app.app_context():
                    sse.publish({
                        'tipo': 'Produtos sem saída',
                        'mensagem': f'O(s) produto(s) com código {sem_saida} não tiveram saída nos últimos {self.minutos} minutos'
                    }, type='message')

            time.sleep(60*self.minutos)

    def Cadastrar(self, request, context):
        return gestor_de_estoque_pb2.SseUrl(url=self.sse_url)

    def ObterRelatorioEstoque(self, request, context):
        ret = dict()
        for (codigo, quantidade) in self.estoque.items():
            if quantidade > 0:
                ret[codigo] = quantidade

        return gestor_de_estoque_pb2.RelatorioEstoque(estoque=ret)

    def ObterRelatorioFluxoMovimentacoes(self, request, context):
        ret = []

        for (momento, movimentacao) in self.historico.items():
            if momento > request.inicio_periodo and momento < request.fim_periodo:
                ret.append(movimentacao)
        
        return gestor_de_estoque_pb2.RelatorioFluxoMovimentacoes(movimentacoes=ret)

    def ObterRelatorioSemSaida(self, request, context):
        ret = []
        com_saida = set()
        for (momento, movimentacao) in self.historico.items():
            if momento > request.inicio_periodo and momento < request.fim_periodo:
                if movimentacao.tipo == "Saída":
                    com_saida.add(movimentacao.codigo)
        
        ret = set(self.produtos_cadastrados.keys()) - com_saida

        return gestor_de_estoque_pb2.RelatorioSemSaida(codigos_sem_saida=list(ret))

    def LancarEntrada(self, request, context):
        data = datetime.now().astimezone().isoformat()

        movimentacao = gestor_de_estoque_pb2.RelatorioFluxoMovimentacoes.Movimentacao(
            tipo='Entrada',
            codigo=request.codigo,
            quantidade=request.quantidade,
            data_movimentacao=data,
            nome=request.nome,
            descricao=request.descricao,
            preco_unitario=request.preco_unitario,
            estoque_minimo=request.estoque_minimo,
        )

        codigo = request.codigo
        # cadastra novo produto internamente
        if codigo not in self.produtos_cadastrados.keys():
            produto = {
                'codigo': codigo,
                'data_cadastro': data,
                'nome': request.nome,
                'descricao': request.descricao,
                'preco_unitario': request.preco_unitario,
                'estoque_minimo': request.estoque_minimo,
            }
            self.produtos_cadastrados[codigo] = produto
            self.estoque[codigo] = request.quantidade
        else:
            self.estoque[codigo] += request.quantidade
        
        # checa se o estoque é menor que o mínimo cadastrado
        if self.estoque[codigo] < self.produtos_cadastrados[codigo]['estoque_minimo']:
            # envia notificação SSE sobre estoque mínimo
            with app.app_context():
                sse.publish({
                    'tipo': 'Estoque mínimo atingido',
                    'mensagem': f'O produto de código "{codigo}" tem {self.estoque[codigo]} de estoque, menor que o estoque mínimo de {self.produtos_cadastrados[codigo]["estoque_minimo"]}'
                }, type='message')
        
        self.historico[data] = movimentacao

        return gestor_de_estoque_pb2.EstadoResposta(estado='ok')

    def LancarSaida(self, request, context):
        data = datetime.now().astimezone().isoformat()

        movimentacao = gestor_de_estoque_pb2.RelatorioFluxoMovimentacoes.Movimentacao(
            tipo='Saída',
            codigo=request.codigo,
            quantidade=request.quantidade,
            data_movimentacao=data,
        )

        codigo = request.codigo
        if codigo not in self.produtos_cadastrados.keys():
            return gestor_de_estoque_pb2.EstadoResposta('produto não cadastrado')
        else:
            self.estoque[codigo] -= request.quantidade

        # checa se o estoque é menor que o mínimo cadastrado
        if self.estoque[codigo] < self.produtos_cadastrados[codigo]['estoque_minimo']:
            # envia notificação SSE sobre estoque mínimo
            with app.app_context():
                sse.publish({
                    'tipo': 'Estoque mínimo atingido',
                    'mensagem': f'''O produto de código "{codigo}" tem {self.estoque[codigo]} de estoque, menor que o estoque mínimo de {self.produtos_cadastrados[codigo]["estoque_minimo"]}'''
                }, type='message')
        
        self.historico[data] = movimentacao

        return gestor_de_estoque_pb2.EstadoResposta(estado='ok')

def serve():
    flask_th = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000, 'debug': False, 'use_reloader': False})
    flask_th.daemon = True
    flask_th.start()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gestor_de_estoque_server = GestorDeEstoqueServicer(minutos=2)
    gestor_de_estoque_pb2_grpc.add_GestorDeEstoqueServicer_to_server(
        gestor_de_estoque_server,
        server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    notification_thread = threading.Thread(target=gestor_de_estoque_server.checaNotificacaoSemSaida)
    notification_thread.daemon = True
    notification_thread.start()
    print("Servidor Pronto")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()