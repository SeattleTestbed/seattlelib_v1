# Check to see if recv will get a socket timeout...

from repyportability import *
import repyhelper
repyhelper.translate_and_import('sockettimeout.repy')
def foo(ip, port, sockobj, ch, mainch):
  # do nothing
  pass

mainch = timeout_waitforconn('127.0.0.1', 12345, foo)
so = timeout_openconn('127.0.0.1', 12345)
try:
  so.recv(1024)
except SocketTimeoutError:
  # great!
  pass
else:
  print "shouldn't get here"

stopcomm(mainch)
exitall()
