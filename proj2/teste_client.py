# saved as greeting-client.py
import Pyro5.api
import threading
import time
import json
import argparse
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, utils, padding

Pyro5.config.SERIALIZER = 'marshal'

# usa módulo argparse do python para descrever argumentos do programa
parser = argparse.ArgumentParser(description='Cliente teste')
parser.add_argument('--debug', action='store_true', help='Escreve informações de debug')

args = parser.parse_args()

# função que só imprime o que foi mandado caso a opção debug esteja ativada
def debug_print(s):
    if args.debug:
        print(s)

class Client(object):
    def __init__(self, name, daemon, server_proxy):
        self.notified = False
        self.daemon = daemon
        self.server_proxy = server_proxy
        self.name = name
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()
        self.serialized_public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
        self.prompts = dict()
        self.prompts["comando"] = ">> "
        self.prompts["entrada"] = "Entrada>> "
        self.prompts["saida"] = "Saída>> "
        self.prompts["relatorio"] = "Relatório>> "
        self.prompts["sair"] = ""

        self.states_entry = dict()
        self.states_entry["comando"] = self.default_entry
        self.states_entry["entrada"] = self.entrada_entry
        self.states_entry["saida"] = self.saida_entry
        self.states_entry["relatorio"] = self.default_entry

        self.states = dict()
        self.states["comando"] = self.comando
        self.states["entrada"] = self.entrada
        self.states["saida"] = self.saida
        self.states["relatorio"] = self.relatorio
    
    def default_entry(self):
        self.prompt = self.prompts[self.state]
        pass
    
    def comando(self, msg):
        # processa comando
        tokens = msg.split()
        if tokens[0] == 'entrada' or tokens[0] == 'e':
            return "entrada"
        elif tokens[0] == 'saida' or tokens[0] == 's':
            return "saida"
        elif tokens[0] == 'relatorio' or tokens[0] == 'r':
            return "relatorio"
        elif tokens[0] == 'help' or tokens[0] == 'h':
            # self.help()
            return "comando"
        elif tokens[0] == 'quit' or tokens[0] == 'q':
            return "sair"
        else:
            return "comando"

    def entrada_entry(self):
        self.entrada_fields = ["Código", "Nome", "Descrição", "Quantidade", "Preço Unitário", "Estoque Mínimo"]
        self.entrada_state = 0
        self.entrada_data = dict()
        self.prompt = self.prompts["entrada"] + self.entrada_fields[self.entrada_state] + ">> "

    def entrada(self, msg):
        self.entrada_data[self.entrada_fields[self.entrada_state]] = msg
        self.entrada_state += 1
        if self.entrada_state >= len(self.entrada_fields):
            # irá enviar mensagem
            message = json.dumps(self.entrada_data)
            message_bytes = bytes(message, 'utf-8')
            signature = self.private_key.sign(
                message_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            debug_print(f"sending message")
            debug_print(self.entrada_data)
            self.server_proxy.lancamento_entrada(self.name, message, signature)
            return "comando"
        
        self.prompt = self.prompts["entrada"] + self.entrada_fields[self.entrada_state] + ">> "
        return "entrada"
    
    def saida_entry(self):
        self.saida_fields = ["Código", "Quantidade"]
        self.saida_state = 0
        self.saida_data = dict()
        self.prompt = self.prompts["saida"] + self.saida_fields[self.saida_state] + ">> "

    def saida(self, msg):
        self.saida_data[self.saida_fields[self.saida_state]] = msg
        self.saida_state += 1
        if self.saida_state >= len(self.saida_fields):
            # irá enviar mensagem
            message = json.dumps(self.saida_data)
            message_bytes = bytes(message, 'utf-8')
            signature = self.private_key.sign(
                message_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            debug_print(f"sending message")
            debug_print(self.saida_data)
            self.server_proxy.lancamento_saida(self.name, message, signature)
            return "comando"
        
        self.prompt = self.prompts["saida"] + self.saida_fields[self.saida_state] + ">> "
        return "saida"
    
    def relatorio(self, msg):
        if msg == '':
            return "comando"
        
        resp = json.loads(self.server_proxy.relatorio(self.name))
        debug_print(f"receiving report")
        debug_print(resp)
        return "relatorio"
    
    @Pyro5.api.expose
    @Pyro5.api.callback
    def callback(self, n):
        self.notified = True
        print(n)

    def run(self):
        # print(type(self.serialized_public_key))
        # print(self.serialized_public_key)
        self.server_proxy.sign_up(self.name, self.serialized_public_key, self.daemon.uriFor(self))
        self.state = ""
        next_state = "comando"
        while next_state != "sair":
            if next_state != self.state:
                self.state = next_state
                self.states_entry[self.state]()

            # indica tópico atual
            print(self.prompt, end='')

            # recebe comando/mensagem
            try:
                msg = input()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            # processa o que foi recebido
            next_state = self.states[self.state](msg)

server = Pyro5.api.Proxy("PYRONAME:example.server")    # use name server object lookup uri shortcut

daemon = Pyro5.server.Daemon()         # make a Pyro daemon
client = Client('client', daemon, server)
client_uri = daemon.register(client)   # register the greeting maker as a Pyro object

th = threading.Thread(target=daemon.requestLoop)
th.daemon = True
th.start()
client.run()