# saved as greeting-client.py
import Pyro5.api

@Pyro5.api.expose
class Cli(object):
    @Pyro5.api.callback
    def callback(self, n):
        print(n)


daemon = Pyro5.server.Daemon()         # make a Pyro daemon
client = Cli()
client_uri = daemon.register(client)   # register the greeting maker as a Pyro object


server = Pyro5.api.Proxy("PYRONAME:example.server")    # use name server object lookup uri shortcut
server.req_callback(client, 25)
server.req_callback(client, 10)

print("ok")
daemon.requestLoop()