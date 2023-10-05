from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, utils, padding
import Pyro5.api
import time
from  datetime import datetime
import json

Pyro5.config.SERIALIZER = 'marshal'

@Pyro5.api.expose
class Serv(object):
    def __init__(self):
        self.proxies = dict()
        self.public_keys = dict()
        self.book = []

    @Pyro5.api.oneway
    def req_callback(self, callback, num):
        # callback._pyroClaimOwnership()
        time.sleep(5 + num/5)
        proxy = Pyro5.api.Proxy(callback)
        proxy.callback(num)

    def sign_up(self, name, public_key, uri):
        # print(name)
        # print(public_key)
        # print(uri)
        self.proxies[name] = Pyro5.api.Proxy(uri)
        self.public_keys[name] = serialization.load_pem_public_key(bytes(public_key, 'utf-8'))
        pass

    def relatorio(self, name):
        return json.dumps(self.book)

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
        obj["datetime"] = date
        print(obj)
        self.book.append(obj)
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
        obj["datetime"] = date
        print(obj)
        self.book.append(obj)
        pass

server = Serv()

daemon = Pyro5.server.Daemon()         # make a Pyro daemon
ns = Pyro5.api.locate_ns()             # find the name server
uri = daemon.register(server)          # register the greeting maker as a Pyro object
ns.register("example.server", uri)     # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls