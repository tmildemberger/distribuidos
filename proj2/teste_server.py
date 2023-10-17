from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, utils, padding
import Pyro5.api
import threading
import time
from  datetime import datetime, timedelta
import json
from queue import Queue

Pyro5.config.SERIALIZER = 'marshal'

@Pyro5.api.expose
class Server(object):
    def __init__(self):
        self.proxies = dict()
        self.public_keys = dict()
        self.produtos_cadastrados = dict()
        self.estoque = dict()
        self.historico = dict()

        self.comandos = Queue()

    # @Pyro5.api.oneway
    # def req_callback(self, callback, num):
    #     # callback._pyroClaimOwnership()
    #     time.sleep(5 + num/5)
    #     proxy = Pyro5.api.Proxy(callback)
    #     proxy.callback(num)

    def sign_up(self, name, public_key, uri):
        # print(name)
        # print(public_key)
        # print(uri)
        self.comandos.put({
            'tipo': 'adicionar_proxy',
            'nome': name,
            'uri': uri
        })

        # self.proxies[name] = Pyro5.api.Proxy(uri)
        self.public_keys[name] = serialization.load_pem_public_key(bytes(public_key, 'utf-8'))
        pass

    def relatorio_estoque(self, name):
        ret = dict()
        for (codigo, quantidade) in self.estoque.items():
            if quantidade > 0:
                ret[codigo] = quantidade
                
        return ret
    
    def relatorio_historico(self, name, start_date, end_date):
        ret = []
        for (data, obj) in self.historico.items():
            if data > start_date and data < end_date:
                ret.append(obj)
                
        return ret
    
    def relatorio_sem_saida(self, name, start_date, end_date, include_out_of_stock=True):
        ret = []
        com_saida = set()
        for (data, obj) in self.historico.items():
            if data > start_date and data < end_date:
                if obj["Tipo"] == "Saída":
                    com_saida.add(obj["Código"])
                
        ret = set(self.produtos_cadastrados.keys()) - com_saida
        if not include_out_of_stock:
            out_of_stock = set()
            for (codigo, quantidade) in self.estoque.items():
                if quantidade == 0:
                    out_of_stock.add(codigo)

            ret = ret - out_of_stock

        return ret

    def lancamento_entrada(self, name, message, signature):
        date = datetime.now().isoformat()
        # try:
        message_bytes = bytes(message, 'utf-8')
        self.public_keys[name].verify(
            signature,
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        obj = json.loads(message)

        codigo = obj['Código']
        nome = obj['Nome']
        descricao = obj['Descrição']
        quantidade = int(obj['Quantidade'])
        preco = obj['Preço Unitário']
        estoque_min = int(obj['Estoque Mínimo'])

        if codigo not in self.produtos_cadastrados.keys():
            produto = {
                'codigo': codigo,
                'nome': nome,
                'descricao': descricao,
                'preco_unitario': preco,
                'estoque_min': estoque_min,
                'data_cadastro': date,
            }
            self.produtos_cadastrados[codigo] = produto
            self.estoque[codigo] = quantidade
        else:
            self.estoque[codigo] += quantidade
        
        if self.estoque[codigo] < self.produtos_cadastrados[codigo]['estoque_min']:
            # notificação
            # print("Notificacao entrada")
            self.comandos.put({
                'tipo': 'notifica',
                'titulo': 'Estoque Mínimo',
                'mensagem': f'Quantidade do produto {codigo} menor que estoque mínimo ({self.estoque[codigo]} < {self.produtos_cadastrados[codigo]["estoque_min"]})'
            })
            pass
        obj['Tipo'] = 'Entrada'
        self.historico[date] = obj
        pass

    def lancamento_saida(self, name, message, signature):
        date = datetime.now().isoformat()
        # try:
        message_bytes = bytes(message, 'utf-8')
        self.public_keys[name].verify(
            signature,
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        obj = json.loads(message)
        #obj["datetime"] = date
        #print(obj)

        codigo = obj['Código']
        quantidade = int(obj['Quantidade'])

        if codigo not in self.produtos_cadastrados.keys():
            print("Ignorando produto não cadastrado")

        self.estoque[codigo] -= quantidade
        if self.estoque[codigo] < self.produtos_cadastrados[codigo]['estoque_min']:
            # notificação
            # print("Notificacao saida")
            self.comandos.put({
                'tipo': 'notifica',
                'titulo': 'Estoque Mínimo',
                'mensagem': f'Quantidade do produto {codigo} menor que estoque mínimo ({self.estoque[codigo]} < {self.produtos_cadastrados[codigo]["estoque_min"]})'
            })
            pass
        obj['Tipo'] = 'Saída'
        self.historico[date] = obj
        pass

    def _notifica(self, tipo, mensagem):
        to_delete = []
        for name, proxy in self.proxies.items():
            try:
                proxy.notificacao(tipo, mensagem)
            except Exception:
                to_delete.append(name)
                pass
        
        for name in to_delete:
            del self.proxies[name]

    def _timer(self):
        while True:
            time.sleep(60)
            self.comandos.put({
                'tipo': 'timer'
            })

    def _run(self):
        while True:
            cmd = self.comandos.get()
            if cmd['tipo'] == 'timer':
                now = datetime.now()
                delta = timedelta(minutes=2)
                print(f"Investigando período entre {(now-delta).isoformat()} e {now.isoformat()}")

                a = self.relatorio_sem_saida('', (now-delta).isoformat(), now.isoformat(), include_out_of_stock=False)
                if len(a) > 0:
                    self._notifica('Promoção', str(a))

            elif cmd['tipo'] == 'adicionar_proxy':
                self.proxies[cmd['nome']] = Pyro5.api.Proxy(cmd['uri'])
            elif cmd['tipo'] == 'notifica':
                self._notifica(cmd['titulo'], cmd['mensagem'])

server = Server()

daemon = Pyro5.server.Daemon()         # make a Pyro daemon
ns = Pyro5.api.locate_ns()             # find the name server
uri = daemon.register(server)          # register the greeting maker as a Pyro object
ns.register("example.server", uri)     # register the object with a name in the name server

print("Ready.")
th = threading.Thread(target=daemon.requestLoop)
th.daemon = True
th.start()

timer_th = threading.Thread(target=Server._timer, args=(server,))
timer_th.daemon = True
timer_th.start()

server._run()