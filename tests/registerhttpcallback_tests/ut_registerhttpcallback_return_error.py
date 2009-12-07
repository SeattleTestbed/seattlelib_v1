# tests a if the registorhttpcallback sends an error msg when a callback fucnc client returns 
# unsuported type

# prints failed message if the test failes and raises an exception the registorhttpcallback
# or httpretrieve raises an exception and just excutes if the test passes


include registerhttpcallback.repy
include httpretrieve.repy


def test_callbackfunc_error(httprequest_dictionary):
  # client that returns wrong type to the registorhttpcallback(returns types are supose to be str only)   
  return 1234
   

    
if callfunc == 'initialize':

  try:
    # register the callback that should send http error 500 for the callback client retruning wrong type  
    handle = registerhttpcallback('http://127.0.0.1:12345', test_callbackfunc_error)
  except Exception, e:
    # raise an exception if the registorhttpcallback raises an exception and stop the server
    stop_registerhttpcallback(handle)
    raise Exception('failed test: server raised an exception: ' + str(e))
    
  
  # send a request to receive the content sent from the server
  try:  
    recvd_content = httpretrieve_get_string('http://127.0.0.1:12345') 
  except HttpError500, e:
    # check if the registorhttpcallback sent the right error msg
    if 'callback func didnt return str' not in str(e):
      print 'failed test: server sent a different an error: ' + str(e)
  except Exception, e:
    # print an failed message if the client recieves a differnt error msg
    print 'httpretrieve raised an exception: ' + str(e)  

  finally:
    # stop the server
    stop_registerhttpcallback(handle)
