# saved as greeting-client.py
import Pyro5.api
import threading
import time

@Pyro5.api.expose
class Cli(object):
    def __init__(self):
        self.notified = False
        
    @Pyro5.api.callback
    def callback(self, n):
        self.notified = True
        print(n)

    def requests(self, server):
        while True:
            server.req_callback(self, 5)
            while not self.notified:
                pass
            self.notified = False
            print("notified")
            time.sleep(2)


daemon = Pyro5.server.Daemon()         # make a Pyro daemon
client = Cli()
client_uri = daemon.register(client)   # register the greeting maker as a Pyro object


server = Pyro5.api.Proxy("PYRONAME:example.server")    # use name server object lookup uri shortcut
#server.req_callback(client, 25)
#server.req_callback(client, 10)

print("ok")
#daemon.requestLoop()
th = threading.Thread(target=daemon.requestLoop)
th.start()
client.requests(server)