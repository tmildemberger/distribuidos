import Pyro5.api
import time

@Pyro5.api.expose
class Serv(object):
    @Pyro5.api.oneway
    def req_callback(self, callback, num):
        callback._pyroClaimOwnership()
        time.sleep(5 + num/5)
        callback.callback(num)

daemon = Pyro5.server.Daemon()         # make a Pyro daemon
ns = Pyro5.api.locate_ns()             # find the name server
uri = daemon.register(Serv)   # register the greeting maker as a Pyro object
ns.register("example.server", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls