# checks if httpretrieve raises an exception when the http header is too long


include httpretrieve.repy


def runhttpserver(ip, port, client_conn, thiscommhandle, listencommhandle):
  # this is a web server like program, doesnt preform some fuctionality's of a server
  # it doesnt check the request  because for this case we know that httpretrieve
  # request, is always to get the http content
  try:
    # recieve http request from http client request
    request = client_request(client_conn) 
    # make a http response including the http header and http content 
    reply = httpresponse(request)
    # send the response
    send_reply(reply, client_conn)
  except Exception, e:
    print 'Error while running the webserver like test:  ' + str(e)



def client_request(client_conn):
  # recieve the http request from the client; we will not be using the request because
  # for this case the http request is always 
  msg_recvd = ""
  while True:
    temp_recvd = client_conn.recv(1)
    msg_recvd += temp_recvd
    # when the http client is done with the http request, it uses a empty line as a
    # signal (\r\n\r\n on some computers and \n\n on others)
    if '\r\n\r\n' in msg_recvd: 
      return msg_recvd 
    if '\n\n' in msg_recvd:
      return msg_recvd

    

def httpresponse(request):
  # http client knows when the http header is done using the empty line signal,
  # if we send a long message with no empty line the http client will read every
  # thing as a header. if 3000 charactor is exceeded httpretrieve shoul raise an
  # exception
  longhttpheader = ' '
  for i in range(5000):
    longhttpheader += str(i)
  return longhttpheader




def send_reply(response, client_conn):
  # Sends response arguement to a client via the client connection and then closes it.
  MAXIMUM_MSG_SIZE = 1024	  
  count = 0
  length_of_msg = len(response)
  while(count < length_of_msg):
    string_to_send = ''
    max = count + MAXIMUM_MSG_SIZE
    if(max >= length_of_msg):
      string_to_send = response[count: ]
    else:
      string_to_send = response[count:max]
    num_sent = client_conn.send(string_to_send)
    count += num_sent
  client_conn.close()




if callfunc == 'initialize':
  # waiting for a connection to start up the web server like program  
  listencommhandle = waitforconn('127.0.0.1', 12345, runhttpserver)
  failed_msg = 'failed: should have raised a exception for the http header length exceeding'
  
  try:
    # set up the http retrieve with a http header to be 5
    recv_msg = httpretrieve_get_string('http://127.0.0.1:12345/', None, None, None, 30, 30, 5)
  except HttpHeaderFormatError, e:
    if 'Http header length Error' not in str(e):
      print failed_msg + ' Raised: ' + str(e) 
    pass
  except Exception, e:
    print failed_msg + ' Raised: ' + str(e) 
  else:
    print failed_msg
  stopcomm(listencommhandle)   
