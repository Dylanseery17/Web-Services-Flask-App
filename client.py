from xmlrpc.server import SimpleXMLRPCServer
def getTemp(val):
    if val <= 10:
        return "cold"
    else:
        return "warm"

server = SimpleXMLRPCServer(("127.0.0.1", 8001))
print("Listening on port 8001...")
server.register_function(getTemp, "getTemp")
server.serve_forever()