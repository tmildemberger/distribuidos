import grpc
import gestor_de_estoque_pb2
import gestor_de_estoque_pb2_grpc

class GestorDeEstoqueServicer(gestor_de_estoque_pb2_grpc.GestorDeEstoqueServicer):
    """Classe que implementa todas as RPCs do arquivo .proto."""
    
    def __init__(self):
        # variáveis para controle do estoque em si
        self.produtos_cadastrados = dict()
        self.estoque = dict()
        self.historico = dict()
        self.sse_url = ''

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

        return gestor_de_estoque_pb2.RelatorioSemSaida(list(ret))

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
            self.estoque[codigo] = quantidade
        else:
            self.estoque[codigo] += quantidade
        
        # checa se o estoque é menor que o mínimo cadastrado
        if self.estoque[codigo] < self.produtos_cadastrados[codigo]['estoque_minimo']:
            # envia comando para outra thread notificar gestores de estoque
            pass
        
        self.historico[data] = movimentacao

    def LancarSaida(self, request, context):

