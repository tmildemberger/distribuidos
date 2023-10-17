# bibliotecas do python
import argparse
import json
import threading
import time

from datetime import datetime, timedelta
from queue import Queue

import Pyro5.api

# biblioteca cryptography para assinatura e verificação com chaves rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, utils, padding

# configura uso do serializer 'marshal'
Pyro5.config.SERIALIZER = 'marshal'

# usa módulo argparse do python para descrever argumentos do programa
parser = argparse.ArgumentParser(description='Servidor do gerenciador de estoque')
parser.add_argument('--debug', action='store_true', help='Escreve informações de debug')

args = parser.parse_args()

# função que só imprime o que foi mandado caso a opção debug esteja ativada
def debug_print(s):
    if args.debug:
        print(s)

# permite que métodos que não começam com '_' sejam acessados por objetos externos
# que possuam a uri do servidor
@Pyro5.api.expose
class Server(object):
    def __init__(self):
        # associa nome de processo externo a um proxy (para notificar de volta);
        # criado e possuido somente pelo thread que notifica (não no do daemon do Pyro, que responde)
        self.proxies = dict()

        # associa nome de processo externo à sua chave pública
        self.chaves_publicas = dict()

        # variáveis para controle do estoque em si
        self.produtos_cadastrados = dict()
        self.estoque = dict()
        self.historico = dict()

        # fila de comandos enviados do thread do Pyro para o thread principal
        self.comandos = Queue()

    # função para o cadastro do gestor de estoque
    def cadastro(self, nome, chave_publica, uri):
        # manda comando para que o outro thread crie o proxy
        self.comandos.put({
            'tipo': 'adicionar_proxy',
            'nome': nome,
            'uri': uri
        })

        # a chave vem no formato PEM, serializado pela própria biblioteca
        self.chaves_publicas[nome] = serialization.load_pem_public_key(bytes(chave_publica, 'utf-8'))

    # gera relatório de estoque, retornando um dicionário que associa um código
    # de produto à seu estoque (quando houver estoque)
    def relatorio_estoque(self):
        ret = dict()
        for (codigo, quantidade) in self.estoque.items():
            if quantidade > 0:
                ret[codigo] = quantidade
                
        return ret
    
    # gera relatório com fluxo de movimentações no período especificado
    def relatorio_fluxo_movimentacoes(self, momento_ini, momento_fim):
        ret = []
        for (momento, movimentacao) in self.historico.items():
            if momento > momento_ini and momento < momento_fim:
                ret.append(movimentacao)
                
        return ret
    
    # gera relatório com produtos sem saída no período especificado
    # (opcionalmente excluindo os que já não tem estoque)
    def relatorio_sem_saida(self, momento_ini, momento_fim, inclui_sem_estoque=True):
        ret = []
        com_saida = set()
        for (momento, movimentacao) in self.historico.items():
            if momento > momento_ini and momento < momento_fim:
                if movimentacao["Tipo"] == "Saída":
                    com_saida.add(movimentacao["Código"])
        
        ret = set(self.produtos_cadastrados.keys()) - com_saida
        if not inclui_sem_estoque:
            sem_estoque = set()
            for (codigo, quantidade) in self.estoque.items():
                if quantidade == 0:
                    sem_estoque.add(codigo)

            ret = ret - sem_estoque

        return ret

    def lancamento_entrada(self, nome, mensagem, assinatura):
        data = datetime.now().isoformat()
        try:
            mensagem_bytes = bytes(mensagem, 'utf-8')
            self.chaves_publicas[nome].verify(
                assinatura,
                mensagem_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            movimentacao = json.loads(mensagem)
        except Exception:
            # caso a assinatura não possa ser verificada, não ocorre o lançamento
            return

        codigo = movimentacao['Código']
        nome = movimentacao['Nome']
        descricao = movimentacao['Descrição']
        quantidade = int(movimentacao['Quantidade']) if movimentacao['Quantidade'].isdecimal() else 0
        preco = movimentacao['Preço Unitário']
        estoque_min = int(movimentacao['Estoque Mínimo']) if movimentacao['Estoque Mínimo'].isdecimal() else 0

        # cadastra novo produto internamente
        if codigo not in self.produtos_cadastrados.keys():
            produto = {
                'codigo': codigo,
                'nome': nome,
                'descricao': descricao,
                'preco_unitario': preco,
                'estoque_min': estoque_min,
                'data_cadastro': data,
            }
            self.produtos_cadastrados[codigo] = produto
            self.estoque[codigo] = quantidade
        else:
            self.estoque[codigo] += quantidade
        
        # checa se o estoque é menor que o mínimo cadastrado
        if self.estoque[codigo] < self.produtos_cadastrados[codigo]['estoque_min']:
            # envia comando para outra thread notificar gestores de estoque
            self.comandos.put({
                'tipo': 'notifica',
                'titulo': 'Estoque Mínimo',
                'mensagem': f'Quantidade do produto {codigo} menor que estoque mínimo ({self.estoque[codigo]} < {self.produtos_cadastrados[codigo]["estoque_min"]})'
            })
        
        # armazena movimentação de entrada
        movimentacao['Tipo'] = 'Entrada'
        self.historico[data] = movimentacao

    def lancamento_saida(self, nome, mensagem, assinatura):
        data = datetime.now().isoformat()
        try:
            mensagem_bytes = bytes(mensagem, 'utf-8')
            self.chaves_publicas[nome].verify(
                assinatura,
                mensagem_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            movimentacao = json.loads(mensagem)
        except Exception:
            # caso a assinatura não possa ser verificada, não reconhece a saída
            return

        codigo = movimentacao['Código']
        quantidade = int(movimentacao['Quantidade']) if movimentacao['Quantidade'].isdecimal() else 0

        if codigo not in self.produtos_cadastrados.keys():
            print("Ignorando produto não cadastrado")

        # diminui quantidade no estoque
        self.estoque[codigo] -= quantidade

        # checa se o estoque ficou menor que o mínimo cadastrado
        if self.estoque[codigo] < self.produtos_cadastrados[codigo]['estoque_min']:
            # envia comando para outra thread notificar gestores de estoque
            self.comandos.put({
                'tipo': 'notifica',
                'titulo': 'Estoque Mínimo',
                'mensagem': f'Quantidade do produto {codigo} menor que estoque mínimo ({self.estoque[codigo]} < {self.produtos_cadastrados[codigo]["estoque_min"]})'
            })
        
        # armazena movimentação de entrada
        movimentacao['Tipo'] = 'Saída'
        self.historico[data] = movimentacao

    # função privada (não exposta) que notifica os proxies cadastrados,
    # e remove o cadastro dos que não é mais possível contactar
    def _notifica(self, tipo, mensagem):
        to_delete = []
        for nome, proxy in self.proxies.items():
            try:
                proxy.notificacao(tipo, mensagem)
            except Exception:
                to_delete.append(nome)
                pass
        
        for nome in to_delete:
            del self.proxies[nome]

    # função privada que envia comando periódico de minuto em minuto
    def _timer(self):
        while True:
            time.sleep(60)
            self.comandos.put({
                'tipo': 'timer'
            })

    # função privada que executa no thread principal, recebendo e executando comandos
    def _run(self):
        while True:
            cmd = self.comandos.get()

            if cmd['tipo'] == 'timer':
                # checa se precisa enviar notificação de promoção
                agora = datetime.now()
                delta = timedelta(minutes=2)
                debug_print(f"Investigando período entre {(agora-delta).isoformat()} e {agora.isoformat()}")

                a = self.relatorio_sem_saida((agora-delta).isoformat(), agora.isoformat(), inclui_sem_estoque=False)
                if len(a) > 0:
                    self._notifica('Produtos Sem Saída (promoção)', str(a))

            elif cmd['tipo'] == 'adicionar_proxy':
                # aqui é que são criados os proxies (pois eles pertencem ao thread que os criou,
                # e só esse thread pode utilizar)
                self.proxies[cmd['nome']] = Pyro5.api.Proxy(cmd['uri'])
            elif cmd['tipo'] == 'notifica':
                # envia notificação de falta de estoque de acordo com o comando
                self._notifica(cmd['titulo'], cmd['mensagem'])

# cria instância da nossa classe servidor
server = Server()

# registra o objeto no daemon
daemon = Pyro5.server.Daemon()
uri = daemon.register(server)

# registra o objeto no servidor de nomes
ns = Pyro5.api.locate_ns()
ns.register("gerenciador_de_estoque.servidor", uri)

debug_print("Ready.")

# inicia thread em background para o loop do daemon do Pyro
th = threading.Thread(target=daemon.requestLoop)
th.daemon = True
th.start()

# inicia thread para a contagem do tempo do nosso servidor
timer_th = threading.Thread(target=Server._timer, args=(server,))
timer_th.daemon = True
timer_th.start()

# inicia função de responder à comandos na thread principal
server._run()