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
        self.prompt = dict()
        self.prompt[0] = ">> "
        self.prompt[1] = "Entrada>> "
        self.prompt[2] = "Saída>> "
        self.prompt[3] = "Relatório>> "
        
    @Pyro5.api.expose
    @Pyro5.api.callback
    def callback(self, n):
        self.notified = True
        print(n)

    def run(self):
        # print(type(self.serialized_public_key))
        # print(self.serialized_public_key)
        self.server_proxy.sign_up(self.name, self.serialized_public_key, self.daemon.uriFor(self))
        state = 0
        while True:
            # self.server_proxy.req_callback(daemon.uriFor(self), 5)
            # while not self.notified:
            #     pass
            # self.notified = False
            # print("notified")
            # time.sleep(2)

            # indica tópico atual
            print(self.prompt[state], end='')

            # recebe comando/mensagem
            try:
                msg = input()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            # processa o que foi recebido
            if len(msg) == 0:
                state = 0
            elif state != 0 and state != 3:
                # irá enviar mensagem
                body = dict()
                body["tipo"] = "entrada" if state == 1 else "saida"
                body["quantidade"] = 2
                message = json.dumps(body)
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
                debug_print(body)
                self.server_proxy.lancamento(self.name, message, signature)
            elif state == 3:
                resp = json.loads(self.server_proxy.relatorio(self.name))
                debug_print(f"receiving report")
                debug_print(resp)
            else:
                # processa comando
                tokens = msg.split()
                if tokens[0] == 'entrada' or tokens[0] == 'e':
                    state = 1
                elif tokens[0] == 'saida' or tokens[0] == 's':
                    state = 2
                elif tokens[0] == 'relatorio' or tokens[0] == 'r':
                    state = 3
                elif tokens[0] == 'help' or tokens[0] == 'h':
                    self.help()
                elif tokens[0] == 'exit' or tokens[0] == 'e':
                    return

server = Pyro5.api.Proxy("PYRONAME:example.server")    # use name server object lookup uri shortcut

daemon = Pyro5.server.Daemon()         # make a Pyro daemon
client = Client('client', daemon, server)
client_uri = daemon.register(client)   # register the greeting maker as a Pyro object

th = threading.Thread(target=daemon.requestLoop)
th.daemon = True
th.start()
client.run()