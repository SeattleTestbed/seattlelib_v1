# tests a if the registorhttpcallback sends an exception, if client raises invalid redirect
# or redirect with no location in callback function

# prints failed message if the test failes and raises an exception the registorhttpcallback
# or httpretrieve raises an exception and just excutes if the test passes


include registerhttpcallback.repy
include httpretrieve.repy


def test_nolocation_redirect(httprequest_dictionary):
  # client that raises a redirect with no location(location should be inputed inside the excetpion)   
  raise HttpError302()

def test_invalidlocation_redirect(httprequest_dictionary):
  # client that returns wrong type to the registorhttpcallback(redirection should input correct format url)   
  raise HttpError302('google')
   

    
if callfunc == 'initialize':

  try:
    # register the callback that redirects with no location  
    handle1 = registerhttpcallback('http://127.0.0.1:12345', test_nolocation_redirect)
    # register the callback that redirects with invalid location
    handle2 = registerhttpcallback('http://127.0.0.2:12345', test_invalidlocation_redirect)
  except Exception, e:  
    print 'failed test: server raised an exception: ' + str(e)

  # make two different requests one at a time to http://127.0.0.1:12345 and http://127.0.0.2:12345
  # because that is the two different ways a client can miss lead redirection
  count = 0   
  while True:
    count += 1  
    # send a request to receive the content sent from the server
    try:
      if count == 1:
        url = 'http://127.0.0.1:12345'
      elif count == 2:
        url = 'http://127.0.0.2:12345'  
      else:
        break 
      # make a request to receive content from the given url
      recvd_content = httpretrieve_get_string(url)
      
    except HttpError500, e:
      # check if the registorhttpcallback sent the right error msg
      if count == 1:
        # for the http://127.0.0.1:12345 which raises a redirect with no location
        if 'callback func client should put the location on raising redirect' not in str(e):
          print 'failed test: server sent a different an error: ' + str(e)
      else:
        # for the http://127.0.0.2:12345 which raises a redirect with a invalid url
        if 'calback func client redirect is invalid' not in str(e):
          print 'failed test: server sent a different an error: ' + str(e)
          
    except Exception, e:
      # print an failed message if the client recieves a differnt error msg
      print 'httpretrieve raised an exception: ' + str(e)  

  # stop both servers
  stop_registerhttpcallback(handle1)
  stop_registerhttpcallback(handle2)
  
