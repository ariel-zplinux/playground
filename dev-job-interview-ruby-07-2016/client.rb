require 'socket'


# read 1024 byte from /dev/urandom
t = IO.binread('/dev/urandom', 1024)

# filter non-utf8
t = t.encode('UTF-8', :invalid => :replace, :undef => :replace)

# open socket
s = TCPSocket.new 'localhost', 2000

# send data
s.write(t)

s.close             # close socket when done
