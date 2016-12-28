require 'socket'

# open socket
server = TCPServer.new 2000 # Server bound to port 2000

# client connected
client = server.accept    # Wait for a client to connect

# read data
r = client.recvmsg

# print data
print r
client.close
