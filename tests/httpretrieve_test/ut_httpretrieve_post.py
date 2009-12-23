# checks if httpretrieve sends the posted data in correct format to a server


# prints failed error msg if httpretrieve failes the test and just excutes if the
# test pass's the test


"""
<Program Name>
  registerhttpcallback.repy

<Started>
  July 29, 2009

<Author>
  Yafete Yemuru

<Purpose>
  This program is Web server that a user can use without understanding http protocol.
  Given a URL this program acts like a web server that places a call back callbackfunc when a
  client(web browser) makes a connection to a given URL. The call back function is meant to
  modify a dynamic page using query and posted data. Once the call back return the modified
  version of the website the registerhttpcallback will complete the process by sending the
  web site content to the client(web browser).

"""


#begin include urllib.repy
def urllib_quote(string, safe="/"):
  """
  <Purpose>
    Encode a string such that it can be used safely in a URL or XML
    document.

  <Arguments>
    string:
           The string to urlencode.

    safe (optional):
           Specifies additional characters that should not be quoted --
           defaults to "/".

  <Exceptions>
    TypeError if the safe parameter isn't an enumerable.

  <Side Effects>
    None.

  <Returns>
    Urlencoded version of the passed string.
  """

  resultstr = ""

  # We go through each character in the string; if it's not in [0-9a-zA-Z]
  # we wrap it.

  safeset = set(safe)

  for char in string:
    asciicode = ord(char)
    if (asciicode >= ord("0") and asciicode <= ord("9")) or \
        (asciicode >= ord("A") and asciicode <= ord("Z")) or \
        (asciicode >= ord("a") and asciicode <= ord("z")) or \
        asciicode == ord("_") or asciicode == ord(".") or \
        asciicode == ord("-") or char in safeset:
      resultstr += char
    else:
      resultstr += "%%%02X" % asciicode

  return resultstr




def urllib_quote_plus(string, safe=""):
  """
  <Purpose>
    Encode a string to go in the query fragment of a URL.

  <Arguments>
    string:
           The string to urlencode.

    safe (optional):
           Specifies additional characters that should not be quoted --
           defaults to the empty string.

  <Exceptions>
    TypeError if the safe parameter isn't a string.

  <Side Effects>
    None.

  <Returns>
    Urlencoded version of the passed string.
  """

  return urllib_quote(string, safe + " ").replace(" ", "+")




def urllib_unquote(string):
  """
  <Purpose>
    Unquote a urlencoded string.

  <Arguments>
    string:
           The string to unquote.

  <Exceptions>
    ValueError thrown if the last wrapped octet isn't a valid wrapped octet
    (i.e. if the string ends in "%" or "%x" rather than "%xx". Also throws
    ValueError if the nibbles aren't valid hex digits.

  <Side Effects>
    None.

  <Returns>
    The decoded string.
  """

  resultstr = ""

  # We go through the string from end to beginning, looking for wrapped
  # octets. When one is found we add it (unwrapped) and the following
  # string to the resultant string, and shorten the original string.

  while True:
    lastpercentlocation = string.rfind("%")
    if lastpercentlocation < 0:
      break

    wrappedoctetstr = string[lastpercentlocation+1:lastpercentlocation+3]
    if len(wrappedoctetstr) != 2:
      raise ValueError("Quoted string is poorly formed")

    resultstr = \
        chr(int(wrappedoctetstr, 16)) + \
        string[lastpercentlocation+3:] + \
        resultstr
    string = string[:lastpercentlocation]

  resultstr = string + resultstr
  return resultstr




def urllib_unquote_plus(string):
  """
  <Purpose>
    Unquote the urlencoded query fragment of a URL.

  <Arguments>
    string:
           The string to unquote.

  <Exceptions>
    ValueError thrown if the last wrapped octet isn't a valid wrapped octet
    (i.e. if the string ends in "%" or "%x" rather than "%xx". Also throws
    ValueError if the nibbles aren't valid hex digits.

  <Side Effects>
    None.

  <Returns>
    The decoded string.
  """

  return urllib_unquote(string.replace("+", " "))




def urllib_quote_parameters(dictionary):
  """
  <Purpose>
    Encode a dictionary of (key, value) pairs into an HTTP query string or
    POST body (same form).

  <Arguments>
    dictionary:
           The dictionary to quote.

  <Exceptions>
    None.

  <Side Effects>
    None.

  <Returns>
    The quoted dictionary.
  """

  quoted_keyvals = []
  for key, val in dictionary.items():
    quoted_keyvals.append("%s=%s" % (urllib_quote(key), urllib_quote(val)))

  return "&".join(quoted_keyvals)




def urllib_unquote_parameters(string):
  """
  <Purpose>
    Decode a urlencoded query string or POST body.

  <Arguments>
    string:
           The string to decode.

  <Exceptions>
    ValueError if the string is poorly formed.

  <Side Effects>
    None.

  <Returns>
    A dictionary mapping keys to values.
  """

  keyvalpairs = string.split("&")
  res = {}

  for quotedkeyval in keyvalpairs:
    # Throw ValueError if there is more or less than one '='.
    quotedkey, quotedval = quotedkeyval.split("=")
    key = urllib_unquote(quotedkey)
    val = urllib_unquote(quotedval)
    res[key] = val

  return res

#end include urllib.repy
#begin include urlparse.repy  
"""
<Program Name>
  urlparse.repy

<Started>
  May 15, 2009

<Author>
  Michael Phan-Ba

<Purpose>
  Provides utilities for parsing URLs, based on the Python 2.6.1 module urlparse.

"""


def urlparse_urlsplit(urlstring, default_scheme="", allow_fragments=True):
  """
  <Purpose>
    Parse a URL into five components, returning a dictionary.  This corresponds
    to the general structure of a URL:
    scheme://netloc/path;parameters?query#fragment.  The parameters are not
    split from the URL and individual componenets are not separated.

    Only absolute server-based URIs are currently supported (all URLs will be
    parsed into the components listed, regardless of the scheme).

  <Arguments>
    default_scheme:
      Optional: defaults to the empty string.  If specified, gives the default
      addressing scheme, to be used only if the URL does not specify one.

    allow_fragments:
      Optional: defaults to True.  If False, fragment identifiers are not
      allowed, even if the URL's addressing scheme normally does support them.

  <Exceptions>
    ValueError on parsing a non-numeric port value.

  <Side Effects>
    None.

  <Returns>
    A dictionary containing:

    Key         Value                               Value if not present
    ============================================================================
    scheme      URL scheme specifier                empty string
    netloc      Network location part               empty string
    path        Hierarchical path                   empty string
    query       Query component                     empty string
    fragment    Fragment identifier                 empty string
    username    User name                           None
    password    Password                            None
    hostname    Host name (lower case)              None
    port        Port number as integer, if present  None

  """

  components = {"scheme": default_scheme, "netloc": "", "path": "", "query": "",
    "fragment": "", "username": None, "password": None, "hostname": None,
    "port": None }

  # Extract the scheme, if present.
  (lpart, rpart) = _urlparse_splitscheme(urlstring)
  if lpart:
    components["scheme"] = lpart

  # Extract the server information, if present.
  if rpart.startswith("//"):
    (lpart, rpart) = _urlparse_splitnetloc(rpart, 2)
    components["netloc"] = lpart

    (components["username"], components["password"], components["hostname"],
      components["port"]) = _urlparse_splitauthority(lpart)

  # Extract the fragment.
  if allow_fragments:
    (rpart, components["fragment"]) = _urlparse_splitfragment(rpart)


  # Extract the query.
  (components["path"], components["query"]) = _urlparse_splitquery(rpart)

  return components


def _urlparse_splitscheme(url):
  """Parse the scheme portion of the URL"""
  # The scheme is valid only if it contains these characters.
  scheme_chars = \
    "abcdefghijklmnopqrstuvwxyz0123456789+-."

  scheme = ""
  rest = url

  spart = url.split(":", 1)
  if len(spart) == 2:

    # Normalize the scheme.
    spart[0] = spart[0].lower()

    # A scheme is valid only if it starts with an alpha character.
    if spart[0] and spart[0][0].isalpha():
      for char in spart[0]:
        if char not in scheme_chars:
          break
      (scheme, rest) = spart

  return scheme, rest


def _urlparse_splitnetloc(url, start=0):
  """Parse the netloc portion of the URL"""

  # By default, the netloc is delimited by the end of the URL.
  delim = len(url)

  # Find the left-most delimiter.
  for char in "/?#":
    xdelim = url.find(char, start)
    if xdelim >= 0:
      delim = min(delim, xdelim)

  # Return the netloc and the rest of the URL.
  return url[start:delim], url[delim:]


def _urlparse_splitauthority(netloc):
  """Parse the authority portion of the netloc"""

  # The authority can have a userinfo portion delimited by "@".
  authority = netloc.split("@", 1)

  # Default values.
  username = None
  password = None
  hostname = None
  port = None

  # Is there a userinfo portion?
  if len(authority) == 2:

    # userinfo can be split into username:password
    userinfo = authority[0].split(":", 1)

    # hostport can be split into hostname:port
    hostport = authority[1].split(":", 1)

    if userinfo[0]:
      username = userinfo[0]
    if len(userinfo) == 2:
      password = userinfo[1]

  # No userinfo portion found.
  else:

    # hostport can be split into hostname:port
    hostport = netloc.split(":", 1)

  # Is there a port value?
  if hostport[0]:
    hostname = hostport[0]
  if len(hostport) == 2:
    port = int(hostport[1], 10)

  # Return the values.
  return username, password, hostname, port


def _urlparse_splitquery(url):
  """Parse the query portion of the url"""

  qpart = url.split("?", 1)
  if len(qpart) == 2:
    query = qpart[1]
  else:
    query = ""

  return qpart[0], query


def _urlparse_splitfragment(url):
  """Parse the query portion of the url"""

  fpart = url.split("#", 1)
  if len(fpart) == 2:
    fragment = fpart[1]
  else:
    fragment = ""

  return fpart[0], fragment

#end include urlparse.repy  
#begin include sockettimeout.repy
"""
<Description>
  Puts back in Python's non-blocking functionality.

  send():
    Raises SocketTimeout Error if the send call lasts
    longer than the set timeout.

  recv():
    Guarentees the receipt of a message.   Raises SocketTimeoutError if it does not
    receive any message before a given timeout.
    If actually receives the message, returns the message and continues.

<Usage>
  Text-replacable for Repy Sockets:
    timeout_openconn(desthost, destport, localip=None, localport=None, timeout = 5)
    timeout_waitforconn(localip, localport, function)

  Object:
    sockobj.settimeout(seconds)
    sockobj.send(data)
    sockobj.recv(bytes)
    sockobj.close()

<Date>
  Sun Mar  1 10:27:35 PST 2009

<Example>
  # hello world
  include sockettimer.repy

  def callback(ip, port, timeout_sockobj, commhandle, listenhandle):
    hw_message = timeout_sockobj.recv(1047)

    # cleanup
    stopcomm(commhandle)
    stopcomm(listenhandle)
    timeout_sockobj.close()

    print hw_message # => "hello world!"
  
  def server():
    sockobj = timeout_waitforconn(getmyip(), 12345, callback)

  def client():
    sockobj = timeout_openconn(getmyip(), 12345)
    sockobj.send("hello world!")

  def main():
    server()
    client()
    exitall()

  if callfunc == 'initialize':
    main() 
"""

class SocketTimeoutError(Exception):
  """The socket timed out before receiving a response"""

def timeout_openconn(desthost, destport, localip=None, localport=None, timeout = 5):
  """
  <Purpose> 
    Wrapper for Repy like socket interface

  <Args>
    Same as Repy openconn

  <Exception>
    Timeout exception if the dest address doesnt respond.

  <Returns>
    socket obj on success
  """

  tsock = TimeoutSocket()
  tsock.settimeout(timeout)
  if localip and localport:
    tsock.bind((localip, localport))
  tsock.connect((desthost, destport))
  return tsock

def timeout_waitforconn(localip, localport, function):
  """
  <Purpose> 
    Wrapper for Repy like socket interface

  <Args>
    Same as Repy waitforconn

  <Side Effects>
    Sets up event listener which calls function on messages.

  <Returns>
    Handle to listener.
  """

  tsock = TimeoutSocket()
  tsock.bind((localip, localport))
  tsock.setcallback(function)
  return tsock.listen()

class TimeoutSocket:
  """
  <Purpose>
    Provide an socket object like the Repy usual one.

  <Side Effects>
    Uses a getlock() to watch for a timeout
    Uses waitforconn and openconn to simulate socket
  """

  ################
  # Constructors
  ################

  def __init__(self):
    """ Constructor for socket """
#    self.lock = getlock() # general lock BUG: Do we need to lock everything?
    self.timeout_lock = getlock() # special lock for Timeout condition
    self.timeout = 5 # seconds to wait
    self.bytes_sent = None # used to check if send() timed out

    # user vars   
    self.local_address = None # ip, port
    self.remote_address = None # ip, port
    self.callback = None # the user's function to call

    # repy socket vars
    self.sockobj = None #  the Repy socket
    self.commhandle = None # the current comm
    self.listencommhandle = None # the listener comm

    #error tracking vars
    
    #if any exceptions are thrown in the separate thread executing _send_and_release, 
    #they are caught and stored in this variable, then raised in _send_or_close
    self.TCPSendError = None

  ################
  # Mutator methods
  #################

  def settimeout(self, value):
    """ Setter for timeout"""
    self.timeout = value

  def setcallback(self, function):
    """ Setter for callback function"""
    self.callback = function

  ####################
  # Public Methods
  ####################

  def bind(self, local_address = None):
    """
    <Purpose>
      Set local address

    <Args>
      Tuple of (ip, port) local.
    """
    self.local_address = local_address

  def listen(self):
    """
    <Purpose>
      Listen for peer
    
    <Side Effects>
      Calls Repy waitforconn()
    """
    return self._waitforconn()

  def connect(self, remote_address):
    """
    <Purpose>
      Connect to peer.

    <Args>
      Tuple of (ip, port) remote.
   
    <Side Effects>
      Calls Repy openconn.
    """
    self.remote_address = remote_address
    self._openconn()

  def recv(self, maxLen): # timeout as optional arg ???
    """
    <Purpose>
      If it fails to finish within the timeout, I close the socket and raise a
      TimeoutError exception. I.e. if there's no message, we call it an error
      and raise it.
      
    <Arguments>
      maxLen - bytes to recv

    <Exception>
      Raises TimeoutError exception if the recv times out
      without receiving a message.

    <Side Effects>
      Closes the connection if times out.

    <Returns>
      The message.
    """
    return self._recv_or_close(maxLen)

  def send(self, data):
    """
    <Purpose>
      Just like normal Repy socket.  Sends messages.
      
    <Arguments>
      data - the string message

    <Exception>
      Same as Repy socket.
 
    <Returns>
      The bytes sent.
    """
    return self._send_or_close(data)

  def close(self):
    self.local_address = None # ip, port
    self.remote_address = None # ip, port
    self.callback = None # the user's function to call

    if self.sockobj:
      self.sockobj.close()
    self.sockobj = None #  the Repy socket
    
    # Armon: As part of the semantics, stopcomm will raise an 
    # exception given an invalid handle, e.g. None. Thus,
    # we need to check for this.
    if self.commhandle: 
      stopcomm(self.commhandle)
      self.commhandle = None # the current comm
    
    # Armon: Same as above.
    if self.listencommhandle:
      stopcomm(self.listencommhandle)
      self.listencommhandle = None # the listener comm


  ########################
  # Private
  #########################

  def _openconn(self):
    """Handle current state variables and call Repy openconn."""

    destip, destport = self.remote_address
    if self.local_address:
      srcip, srcport = self.local_address
      self.sockobj = openconn(destip, destport, srcip, srcport, self.timeout)
    else:
      self.sockobj = openconn(destip, destport)

  def _waitforconn(self):
    """Setup way between Repy waitforconn event"""
    localip, localport = self.local_address
    self.listencommhandle = waitforconn(localip, localport, self._callback)
    return self.listencommhandle

  def _callback(self, ip, port, sockobj, ch, lh):
    """Pass on through to user callback"""
    self.sockobj = sockobj
    self.listencommhandle = lh # same as the 1st from wait for comm, right?
    self.commhandle = ch # should we care?
    
    if not self.remote_address:
      self.remote_address = (ip, port)
    else: 
      raise Exception("what! peer does not match?")

    self.callback(ip, port, self, ch, lh)

  def _send(self, data):
    """Send data"""
    return self.sockobj.send(data)

  def _recv(self, maxLen):
    """Recv data of length maxLen"""
    return self.sockobj.recv(maxLen)

  def _send_and_release(self, data):
    """Send data then release the timeout lock"""
    
    #Bug Fix (Cosmin): exceptions thrown in separate thread _send_and_release could not be caught
    #now we store the exception if it is thrown and raise it back in send_or_close
    try:
      self.bytes_sent = self._send(data)
    except Exception, e:
      self.TCPSendError = e
    
    self._quietly_release() # release the lock
 
  def _quietly_release(self):
    """Release the timeout lock and ignore if already released"""
    try:
      self.timeout_lock.release()
    except:
      pass
   
  def _send_or_close(self, data):
    """Raise the Timeout Error if no receipt.  Keep track by timeout_lock."""

    # acquire the lock, when it's release we'll carry on
    self.timeout_lock.acquire()

    # fork off a lock that'll release the lock at the timeout
    timerhandle = settimer(self.timeout, self._quietly_release, ())

    # fork off a send call so we can raise the exception in the main thread
    # the send call will also release our lock
    settimer(0, self._send_and_release, (data,))

    # block until either the timeout or _send finishes
    self.timeout_lock.acquire()
    self.timeout_lock.release()

    if self.bytes_sent: # send finished
      canceltimer(timerhandle)
      retdata = self.bytes_sent
      self.bytes_sent = None
      return retdata
    elif self.TCPSendError != None:
      #Bug Fix (Cosmin): exceptions thrown in separate thread _send_and_release could not be caught
      
      #we got an error within the separate thread that performed the send operation
      exception_to_throw = self.TCPSendError
      self.TCPSendError = None
      raise exception_to_throw
    else: # it timed out
      self.close()
      raise SocketTimeoutError

  def _recv_or_close(self, amount):
    """Raise the Timeout Error if no receipt.  Keep track by timeout_lock."""
    timerhandle = settimer(self.timeout, self._clobbersocket, ())
    try:
      retdata = self._recv(amount)
    except Exception, e:
      # if it's not the timeout, reraise...
      if self.timeout_lock.acquire(False):
        raise
      raise SocketTimeoutError
    
    # I acquired the lock, I should stop the timer because I succeeded...
    if self.timeout_lock.acquire(False):
      # even if this isn't in time, the lock prevents a race condition 
      # this is merely an optimization to prevent the timer from ever firing...
      canceltimer(timerhandle)
      self.timeout_lock.release() # Alper's bug 3/10/09
      return retdata
    else:
      raise SocketTimeoutError

  def _clobbersocket(self):
    """If I can acquire the lock without blocking, then close the socket to abort"""
    if self.timeout_lock.acquire(False):
      self.close()


############################
# Deprecated functions
##############################

# private function...
def sockettimeout_clobbersocket(sockobj,mylock):
  # if I can acquire the lock without blocking, then close the socket to abort
  if mylock.acquire(False):
    sockobj.close()

# if it fails to finish within the timeout, I close the socket and raise a
# SocketTimeout exception...
def sockettimeout_recv_or_close(sockobj, amount, timeout):
  # A lock I'll use for this attempt
  mylock = getlock()
  timerhandle = settimer(timeout,clobbersocket, (sockobj, mylock))
  try:
    retdata = sockobj.recv(amount)
  except Exception, e:
    # if it's not the timeout, reraise...
    if mylock.acquire(False):
      raise
    raise SocketTimeout
    
  # I acquired the lock, I should stop the timer because I succeeded...
  if mylock.acquire(False):
    # even if this isn't in time, the lock prevents a race condition 
    # this is merely an optimization to prevent the timer from ever firing...
    canceltimer(timerhandle)
    return retdata
  else:
    raise SocketTimeout


#end include sockettimeout.repy
# used for hierarchy exception 
#begin include http_hierarchy_error.repy
"""
<Program Name>
  http_hierarchy_error.repy

<Started>
  Oct 05, 2009

<Author>
  Yafete Yemuru

<Purpose>
  provides a hierachy http error using status code including client and server errors
  classes.  
"""


'''
http hierarchy error exception classes

-> HttpError
   -> HttpRetrieveClientError
      -> HttpUserInputError
      -> HttpConnectionError

   -> HttpServerError
      -> HttpResponseError
         -> HttpHeaderError
            -> HttpHeaderReceivingError
            -> HttpHeaderFormatError
         -> HttpContentError
            -> HttpContentReceivingError
            -> HttpContentLengthError
       
   -> HttpStatuscodeError
     -> HttpError1xx
        -> followed by all http status code error number HttpError(number)
        
     -> HttpError2xx
        -> followed by all http status code error number HttpError(number)
        
     -> HttpError3xx
        -> followed by all http status code error number HttpError(number)

     -> HttpError4xx
        -> followed by all http status code error number HttpError(number)
        
     -> HttpError5xx
        -> followed by all http status code error number HttpError(number)

'''

class HttpError(Exception):
  pass

# raises an exception for http client error 
class HttpRetrieveClientError(HttpError):# extend HttpError 
  pass
class HttpUserInputError(HttpRetrieveClientError):
  pass
class HttpConnectionError(HttpRetrieveClientError):
  pass


# raises an exception for any http server failure  
class HttpServerError(HttpError):# extend HttpError 
  pass
class HttpResponseError(HttpServerError):
  pass
class HttpHeaderError(HttpResponseError):
  pass
class HttpHeaderReceivingError(HttpHeaderError):
  pass
class HttpHeaderFormatError(HttpHeaderError):
  pass
class HttpContentError(HttpResponseError):
  pass
class HttpContentReceivingError(HttpContentError):
  pass
class HttpContentLengthError(HttpContentError):
  pass


class HttpStatusCodeError(HttpError):# extend HttpError
  pass
class HttpError1xx(HttpStatusCodeError):
  pass
class HttpError100(HttpError1xx):
  pass
class HttpError101(HttpError1xx): 
  pass
class HttpError102(HttpError1xx): 
  pass


class HttpError2xx(HttpStatusCodeError):
  pass
class HttpError201(HttpError2xx): 
  pass
class HttpError202(HttpError2xx):   
  pass
class HttpError203(HttpError2xx): 
  pass
class HttpError204(HttpError2xx): 
  pass
class HttpError205(HttpError2xx): 
  pass
class HttpError206(HttpError2xx): 
  pass
class HttpError207(HttpError2xx): 
  pass
class HttpError226(HttpError2xx): 
  pass                 


class HttpError3xx(HttpStatusCodeError):
  pass
class HttpError300(HttpError3xx): 
  pass
class HttpError301(HttpError3xx): 
  pass
class HttpError302(HttpError3xx): 
  pass
class HttpError303(HttpError3xx): 
  pass
class HttpError304(HttpError3xx):
  pass
class HttpError305(HttpError3xx): 
  pass
class HttpError306(HttpError3xx): 
  pass
class HttpError307(HttpError3xx): 
  pass
                    

class HttpError4xx(HttpStatusCodeError):
  pass
class HttpError400(HttpError4xx):
  pass  
class HttpError401(HttpError4xx): 
  pass
class HttpError402(HttpError4xx): 
  pass
class HttpError403(HttpError4xx):
  pass  
class HttpError404(HttpError4xx): 
  pass
class HttpError405(HttpError4xx): 
  pass
class HttpError406(HttpError4xx): 
  pass
class HttpError407(HttpError4xx): 
  pass
class HttpError408(HttpError4xx): 
  pass
class HttpError409(HttpError4xx): 
  pass
class HttpError410(HttpError4xx): 
  pass
class HttpError411(HttpError4xx): 
  pass
class HttpError412(HttpError4xx): 
  pass
class HttpError413(HttpError4xx): 
  pass
class HttpError414(HttpError4xx): 
  pass
class HttpError415(HttpError4xx): 
  pass
class HttpError416(HttpError4xx): 
  pass
class HttpError417(HttpError4xx): 
  pass
class HttpError418(HttpError4xx): 
  pass
class HttpError422(HttpError4xx): 
  pass
class HttpError423(HttpError4xx): 
  pass
class HttpError424(HttpError4xx): 
  pass
class HttpError425(HttpError4xx): 
  pass
class HttpError426(HttpError4xx): 
  pass


class HttpError5xx(HttpStatusCodeError):
  pass
class HttpError500(HttpError5xx): 
  pass
class HttpError501(HttpError5xx): 
  pass
class HttpError502(HttpError5xx): 
  pass
class HttpError503(HttpError5xx): 
  pass
class HttpError504(HttpError5xx): 
  pass
class HttpError505(HttpError5xx): 
  pass
class HttpError506(HttpError5xx):
  pass  
class HttpError507(HttpError5xx):
  pass  
class HttpError510(HttpError5xx):
  pass

#end include http_hierarchy_error.repy





def registerhttpcallback(url, callbackfunc, httprequest_limit = 131072, httppost_limit = 2048):
  """
  <Purpose>
     Waits for a connection to the given url(host). Calls callbackfunc with a argument of http request
     dictionary up on success. 
  
     
  <Arguments>
     url:
           String of a http web server-URL 

     callbackfunc:
            The callbackfunc to be called. It can take up to three argument .
            First argument- The http request dictionary keys are as follows:
              http_command - for the http request method GET or POST
              http_version - which http version the client  used HTTP\1.1 or HTTP\1.0  
              path - the exact request path parsed 
              query - the exact request query parsed 
              posted_data - if there is any posted data returns None if there isnt one

              And all the http requests headers the client provided. eg. Content-Length: 22  
              will incude Content-Length as a key and 22 as a value

            Second argument - httprequest query; this returns a unencoded dictionary of the query
            Third argument - httprequest posted data; this returns a unencoded dictionary of the posted data

            RESTRICTIONS:
              -> Follow the http_hierarchy_error(HttpStatusCodeError)to raise an exception. eg. raise
                  HttpError404 for file not found
              -> To redirect raise HttpError301(url) or HttpError302(url). The url has to be valid.  
              -> server only excepts tuple type of [httpcontent, httpheader] where the httpcontent is a
                  string of the content intended to display. httpheader is a dictionary used only if you have a
                  extra header you want to add on the http response. 

     httprequest_limit:
            -> used to to limit the http request a client can make(default value set to 128kb or 131072 charactors)

     httppost_limit:
            -> used to to limit the http post a client can make(default value set to 2mb or 2048 charactors)     


  <Exceptions>
          HttpConnectionError-> if the server fails on waiting for a connection
          HttpUserInputError -> if server fails on making a connection to client(web browser)
          HttpServerError -> If server fails internally

          HttpError408 -> If client(web browser) takes to long to send request  
          HttpError413 -> If the http posted data length is too long
                       -> If the http request length is too long
          HttpError417 -> If there is the http request format problem
                       -> If the content length doesnt match the actual posted data length
          HttpError501 -> If the given http command is not supported or valid (supported 'GET' and 'POST')
          HttpError411 -> If the http command is POST and content length is not given
          HttpError500 -> If server fails internally on sending the http content OR HTTP header,sending error and
                       -> If the callback fucntion doesnt follow restrictions  
                       -> if the users input for url is not in correct format or unsuported
                          protocol(this program only supports Http)


  <Side Effects>
     None 

  <Returns>
     A handle to the listener. This can be used to stop the server from waiting for a connection.  
  """  
  def run_webserver(ip, port, sock, thiscommhandle, listencommhandle):
  # this function is defined inside the registerhttpcallback fuction so callback function name that is
  # given by a user is placed a call on when there is a connection. 
    try:
      # receive the client(web browser) request and return a list of the request
      client_request_lines = _registerhttpcallback_receive_client_request(sock, httprequest_limit)

      # check if the received request meets http requsest format standards and return a
      # dictionary of the http request headers. 
      httprequest_dictionary = _registerhttpcallback_make_httprequsest_dictionary(client_request_lines)    

      # check if there is posted data and add to the httprequest_dictionary with a key posted_data.
      # returns None if there isnt a posted data
      _registerhttpcallback_receive_httpposted_data(sock, httprequest_dictionary, httppost_limit)
      
      # get dictionary decode from the given query 
      httprequest_query = _registerhttpcallback_get_decode_dict(httprequest_dictionary, 'query')

      # get dictionary decode from the given post 
      httprequest_posted_data = _registerhttpcallback_get_decode_dict(httprequest_dictionary, 'posted_data')

      # place the call back callbackfunc with dictionary that includes http_command,
      # http_version, path, query, posted_data, and all the http requests headers
      webpage_content = callbackfunc(httprequest_dictionary, httprequest_query, httprequest_posted_data)
        
      # callback callbackfunc excecuted, send the processed dynamic web page data to client(web browser)
      _registerhttpcallback_send_httpresponse(sock, webpage_content)

      
    except HttpStatusCodeError, e:
      # send any error that occur during processing server to the client(web browser)
      _registerhttpcallback_send_httpformat_error(sock, e)
      
      
    except Exception, e:
      # if the program failed to catch an internal error raise an exception and send it to client(web browser)
      try:
        raise HttpError500('Server failed internally: ' + str(e))
      except Exception, e:
        _registerhttpcallback_send_httpformat_error(sock, e)



  
  # get the host and port from the given url to use for connection to listen on
  (host, port) = _registerhttpcallback_get_host_port(url)

  try:
    # waits for a client(web browser) to make a connetion and run the web server 
    listencommhandle = waitforconn(host, port, run_webserver)

  except Exception, e:
    # the waiting for a connection failed, stop waiting and raise an exception 
    stopcomm(listencommhandle)
    raise HttpConnectionError('Web server failed on waiting for connection ' + str(e))

  else:
    # store the listencommhandle, to stop server if needed
    return listencommhandle








def stop_registerhttpcallback(handle):   
  """
    <Purpose>
          Deregister a callback for a commhandle. 

    <Arguments>
          commhandle:
              A commhandle as returned by registerhttpcallback.

    <Exceptions>
          None.

    <Side Effects>
          This has an undefined effect on a socket-like object if it is currently in use.

    <Returns>
          Returns True if commhandle was successfully closed, False if the handle cannot be closed 
  """
  #close the connection
  return stopcomm(handle)

   


  

def _registerhttpcallback_get_host_port(url):
  # get host and path from the given url
  try:
    # returns a dictionary of {scheme, netloc, path, quer, fragment, username, password, hostname and port} form the url
    urlparse = urlparse_urlsplit(url)  
  except Exception, e:
    raise HttpUserInputError('Server URL format error:' + str(e))
  else:
    # check if the given url is valid using the url parse 
    if urlparse['scheme'] != 'http':
      raise HttpUserInputError('The given protocol type isnt suported: Given ' + urlparse['scheme'])       
    if urlparse['hostname'] == None:
      raise HttpUserInputError('Server URL format error: host name is not given') 

    host = urlparse['hostname']
    
    # use default port 80 if the port isnt given
    if urlparse['port'] == None:
      port = 80
    else:
      # if given use the given port
      port = urlparse['port']

    return host, port



      
def _registerhttpcallback_receive_client_request(sock, httprequest_limit):
  # receive request from the client using the socket connection
  if not type(httprequest_limit) == int:
    # check if the given httprequest limit is valid
    raise HttpServerError('The given http request limit isnt int ' + str(e))
  
  
  # empty line is used as a signal for when the http request is done, and we set a
  # default request length limit to be 131072 character(128kb)
  client_request = _registerhttpcallback_receive_untilemptyline(sock, httprequest_limit)
        
  
  # http request format requires the request to be line by line
  # build a list of the received request split line by line to check the formating of the request
  client_request_lines = ''
  try: 
    # split the entire message line by line 
    client_request_lines = client_request.splitlines()
  except Exception, e:
    # raise an exception if the request doenst follow the http protocol format 
    raise HttpError417('Error on the http request format ' + str(e))
  
  # the http request has to be at least one line including the http header request
  if len(client_request_lines) == 0:
    raise HttpError417('The received request doesnt follow http protocol requirments: Given ' + client_request)

  # returns a list of client request
  return client_request_lines





def _registerhttpcallback_make_httprequsest_dictionary(client_request_lines):
  # builds up a dictionary from the received request or raises an exception if the
  # request format isnt http protocol. The dictionary also includes the http header request
  # parsed with custome keys (http_command - for http comand methed, path - parsed form
  # the request url, query - query string parsed form the request url, http_version -
  # for the http protocol version)
  
  httpheader_request = True
  httprequest_dictionary = {}
  
  for request_line in client_request_lines:  
    if httpheader_request:
      # acording to the http protocol format the first line is different because it is includes comand url and version

      # check if the http request is valid and parse the http request method, URL and http version
      (http_command, path, query, http_version) = _registerhttpcallback_httprequest_header_parse(request_line)

      # use custom names for the parsed data of the first request line and add to the dictionary 
      httprequest_dictionary['http_command'] = http_command
      httprequest_dictionary['http_version'] = http_version
      httprequest_dictionary['path'] = path
      httprequest_dictionary['query'] = query  

      # used to flag the for the upcoming lines, because they have stationary keys
      httpheader_request = False 
      
    elif request_line == '':
      # last line is empty line, return the http dictionary built so far
      return httprequest_dictionary  

    else:
      # the rest of the lines should be formated 'httpheader_key: httpheader_value'  eg.'Content-Length: 34'
      try:
        modified_request = request_line.split(': ')
      except Exception, e:
        raise HttpError417('Error on the http request format; Given: ' + request_line + 'in the request line ' + str(e))

      # raise an exception if the request line doesnt contain 2 contents for 'httpheader_key: httpheader_value' 
      if len(modified_request) != 2:
        raise HttpError417('Error on the http request format; Given: ' + request_line + 'in the request line')

      httprequest_key = modified_request[0]
      httprequest_value = modified_request[1]
      
      httprequest_dictionary[httprequest_key] = httprequest_value

  return httprequest_dictionary
  




def _registerhttpcallback_get_decode_dict(httprequest_dictionary , decode_type):
  # returns a decode dictionary of post or query depending up on the encoded style   

  # get the data from the request dictionary 
  data_to_decode = httprequest_dictionary[decode_type]
      
  if decode_type == 'posted_data':
    # inorder to check if the post is empty use None   
    empty_check = None    
  else:
    # inorder to check if the query is empty use empty string   
     empty_check = ''
        
  if data_to_decode != empty_check:
    try:
      # decode the given data depending up on the style it was encoded  
      return urllib_unquote_parameters(data_to_decode)

    except Exception, e:
      # raise an exception if the fails decoding the given data  
      raise HttpUserInputError('Invalid ' + decode_type + ' Raised ' + str(e) + ' on decoding')

  # if the data is empty return None 
  return None    




  
def _registerhttpcallback_httprequest_header_parse(http_header_request):
  # varifiy's if the http request header format is valid and returns the http command, path, query,
  # and http version parsed from the http header

  # http request header should include RequestMethod <url> HTTP<version> or RequestMethod HTTP<version>
  # and is located at the top of the http request
  try:
    http_command_url_version = http_header_request.split()
  except Exception, e:
    raise HttpError417('Http header request needs spacing in between: Given: ' + http_header_request + str(e))

  # Check that the first line at least contains 3  words: RequestMethod <url> HTTP<version>
  if len(http_command_url_version) >= 3: 
    url = http_command_url_version[1]
    http_version = http_command_url_version[2]
  
  else:
    # http request header cant have any more data than RequestMethod <url> HTTP<version> or RequestMethod HTTP<version>
    raise HttpError417('The request header should contain  RequestMethod <url> HTTP<version>, Given: ' + http_header_request)

  # check the http comand is valid or if its even suported(suported comands include GET and POST)
  if http_command_url_version[0] == 'GET' or http_command_url_version[0].lower() == 'post':
     http_command = http_command_url_version[0]
  else:
    raise HttpError501('The given http comand is not suported or valid. Given: ' + str(http_command_url_version[0]))
  

  # check the if the http version is valid
  if not http_version.startswith('HTTP'):
    raise HttpError417('Http header request version should start of with HTTP then <version>, Given: ' +  httpversion + ' as a http version') 

  # (query used to modify the dynamic page) http header includes the path and query, pasrse the given url to path and query 
  (path, query) = _registerhttpcallback_parse_httpheader_url(url)  

  return http_command, path, query, http_version 




def _registerhttpcallback_parse_httpheader_url(url):
  # parse out the query and path from the url
  path = ''
  query = ''

  # if url isnt given return empty strings  
  if url != '':
    # if url is given parse the query and path using url parse
    try:
     # returns a dictionary of {scheme, netloc, path, query, fragment, username,
     # password, hostname and port} parsing the url                      
      urlparse = urlparse_urlsplit(url)  
    except Exception, e:
      raise HttpError417('Http request given url doesnt meet the http protocol standards ' + str(e) + 'Given url: ' + url)

    # retrieve only the path and query 
    try:
      path = urlparse['path']
      query = urlparse['query']
    except Exception, e:
      raise HttpError417('Http request given url doesnt meet the http protocol standards ' + str(e) + 'Given url: ' + url)
        
    # if there is a url there has to be a path so raise an exception because the given url format is wrong 
    if path == '':
      raise HttpError417('Error on parsing the http request header url: Given ' + url)
    
  return path, query




def _registerhttpcallback_receive_httpposted_data(sock, httprequest_dictionary, httppoost_limit):
  # receive the posted data which sent right after the http request with a empty line
  # indicating the end of the posted data(this is if the http comand is only a POST)

  if not type(httppoost_limit) == int:
    # check if the given http post limit is valid
    raise HttpServerError('The given http post limit is not a int, given: ' + str(type(httppoost_limit)))

  # if the http comand method isnt post theres is no posted data
  posted_data = None

  # Bug pointed out by Albert Rafetseder: not all browsers send post with caps 
  if httprequest_dictionary['http_command'].lower() == 'post':
    # get the posted data length or raise an exception if not given 
    try:
      posted_data_length = int(httprequest_dictionary['Content-Length'])
    except Exception, e:   
      raise HttpError411('content length is required on a http POST comand')
    else:
      # Bug pointed out by Albert Rafetseder: post doesnt send a empty line after the posted data
      # recieve the posted data using the posted data length
      posted_data = _registerhttpcallback_receive_httppost(sock, posted_data_length, httppoost_limit)

    # check if there is a posted data and return it
    if len(posted_data) == 0:
      raise HttpError417('The request included a http POST comand with no data posted')
    
  # adds the posted data or None to the httprequest dictionary 
  httprequest_dictionary['posted_data'] = posted_data





def _registerhttpcallback_receive_httppost(sock, http_post_length, length_limit):
  # receives posted data from the given connection untill the given content length field matchs the received amount 
  total_recvd_post = ''
  
  while True:
    if len(total_recvd_post) == http_post_length:
      # if the content length matchs the received posted data return it 
      return total_recvd_post

    # raise an exception if the received posted data length is greater than the given http header content length   
    if len(total_recvd_post) > http_post_length:
      raise HttpError417('The http posted data didnt match the http content length header, given content length: ' + str(http_post_length) + ' while posted data length is ' + str(len(total_recvd_post)))

    # raise an exception if the total received length has exceeded the given length limit
    if len(total_recvd_post) > length_limit:                  
      raise HttpError413('The http posted data length exceeded length limit of ' + str(length_limit))

                       
    try:
      # receive one character at a time inorder to check for the empty line
      content = sock.recv(512)

    # catch any error that happens while receiving content             
    except SocketTimeoutError, e:
      raise HttpError408('The server timed out while waiting to receive the post data ' + str(e))
    except Exception, e: 
      raise HttpError500('Error while receiving request posted data ' + str(e))

    else:
      # if there was not receiving error, keep on adding the receieved content 
      total_recvd_post += content



  

def _registerhttpcallback_receive_untilemptyline(sock, length_limit):
  # receives data from socket connection until it a empty line or until the given
  # length limit is exceeded                      
  total_recvd_content = ''
  
  while True:
    # receive until a empty line (\n\n or \r\n\r\n because new line is different by computer) 
    if '\r\n\r\n' in total_recvd_content or '\n\n' in total_recvd_content:
      # found a empty line return the total received content
      return total_recvd_content.strip()

    # raise an exception if the total received length has exceeded the given length limit
    if len(total_recvd_content) > length_limit:                  
      raise HttpError413('The http request length exceeded the given length limit ' + str(length_limit))
                        
    try:
      # receive one character at a time inorder to check for the empty line
      content = sock.recv(1)

    # catch any error that happens while receiving content             
    except SocketTimeoutError, e:
      raise HttpError408('The server timed out while waiting to receive the request ' + str(e))
    except Exception, e: 
      raise HttpError500('Error while receiving http request ' + str(e))

    else:
      # if there was not receiving error, keep on adding the receieved content 
      total_recvd_content += content





def _registerhttpcallback_send_httpresponse(sock, callbackfunc_val):
  # sends a response to the client(web browser) with a ok http header and the http web page content
  if not type(callbackfunc_val) == list:
    raise HttpUserInputError('Callback func didnt return list, returned ' + str(type(callbackfunc_val)))

  try:
    webpage_content = callbackfunc_val[0]
    callbckfunc_httpheader = callbackfunc_val[1]
  except Exception, e:
    raise HttpUserInputError('Callback func returned data failed ' + str(e))

  # check the given web page content 
  if not type(webpage_content) == str:
    raise HttpUserInputError('Callback func didnt return str for the content, returned ' + str(type(webpage_content)))
  if len(webpage_content) == 0:
    raise HttpUserInputError('Callback func didnt return any content')
  
  
  # build the http ok response header 
  httpheader = 'HTTP/1.0 200 OK\n'
  httpheader += 'Content-Length: ' + str(len(webpage_content)) + '\n'
  #check if there is a given http header and add it to the response
  httpheader += _registerhttpcallback_parse_callbckfunc_httpheader(callbckfunc_httpheader)
    
  httpheader += 'Server: Seattle Testbed\n\n'

  # http header followed by http content and close the connection
  try:
    sock.send(httpheader) 
    sock.send(webpage_content)
    sock.close() 
  except Exception, e:
    raise HttpConnectionError('server failed to send the http content ' + str(e))  





def _registerhttpcallback_parse_callbckfunc_httpheader(callbckfunc_httpheader):
  # builds a http header from the given http callback func list
  if callbckfunc_httpheader == None:
    # if the http header isnt given return a empty string
    return ''
  elif not type(callbckfunc_httpheader) == dict:
    # raise an exception if the http header isnt dictionary
    raise HttpUserInputError('The given http header is not a dictionary, given: ' + str(type(callbckfunc_httpheader)))
  else: 
    # take the given key and val from the callbckfunc_httpheader dictionary and add them to the http header with
    # correct http format
    httpheaders = ''
    for key, val in callbckfunc_httpheader.items():
      # make simple checks on the key and val 
      if not type(key) == str:
        raise HttpUserInputError('The callback func given http header key isnt str given ' + str(type(key)))
      if not type(val) == str:
        raise HttpUserInputError('The callback func given http header value isnt str given ' + str( type(val)))
      if key == '' or val == '':
        # raise an exception if the key or value is a empty field
        raise HttpUserInputError('The callback func given empty http header feild of key or value')
      if key.capitalize() != key:
        raise HttpUserInputError('The callback func given http header key is not capitalized, given: ' + key)

      # add the key and value to the http header field
      httpheaders += key + ' : ' + val + '\n'  

    # return the string of the http header  
    return httpheaders

  



def _registerhttpcallback_send_httpformat_error(sock, e):
  # send  correct format http header with a  http content that displays detailed error msg and close connection 

  # using the httpstatuscode dictionary get the statuscode number and statuscode constant from the given httperror
  (statuscode_numb, client_error_msg, statuscode_constant) = _registerhttpcallback_get_http_statuscode(e)
  
  # build http body error msg to client(web browser)
  error_msg = client_error_msg

  # error content body
  httpcontent = '<html>'
  httpcontent += '<head><title>' + str(statuscode_numb) + ' ' + statuscode_constant + '</title></head>'
  httpcontent += '<body><h1>' + str(statuscode_numb) + ' ' + statuscode_constant + '</h1>'
  httpcontent += '<p>' + error_msg + '</p></body>'
  httpcontent += '</html>'
  # to end the error content
  httpcontent += '\n\n'
  
  # build the http header to send    
  httpheader = 'HTTP/1.0 ' + str(statuscode_numb)  + ' ' + statuscode_constant + '\n'

  # for redirect add the location of the redirection to the http header    
  if statuscode_numb == 301 or statuscode_numb == 302:
    if client_error_msg == '':
      raise HttpUserInputError('Internal server error: callback func client should put the location on raising redirect')
    elif not client_error_msg.startswith('http://'):
      raise HttpUserInputError('Internal server error: calback func client redirect is invalid, Given: ' + client_error_msg)
    else:
      httpheader += 'Location: ' + str(client_error_msg) + '\n'
  
  # finish up the http header
  httpheader += 'Content-Length: ' + str(len(httpcontent)) + '\n'
  httpheader += 'Server: Seattle Testbed\n\n'
  
  # send the http response header and body to the client(web browser) and close connection
  try:
    sock.send(httpheader)
    sock.send(httpcontent)
    sock.close()
  except Exception, e:
    raise HttpConnectionError('server failed internally on send http error ' + str(statuscode_numb) + ' ' + statuscode_constant + ' ' + error_msg + ' Raised' + str(e)) 




def _registerhttpcallback_get_http_statuscode(e):
  # retrieves the status code number and constant given a exception class 
  
  # httpstatus code dictionary with the statuscode constant
  httpstatuscode_dict = {
      HttpError100: (100, 'Continue'),
      HttpError101: (101, 'Switching Protocols'),
      HttpError102: (102, 'Processing'),
      HttpError201: (201 ,'Created'),
      HttpError202: (202, 'Accepted'),  
      HttpError203: (203, 'Non-Authoritative Information'),
      HttpError204: (204, 'No Content'),
      HttpError205: (205, 'Reset Content'),
      HttpError206: (206, 'Partial Content'),
      HttpError207: (207, 'Multi-Status'),
      HttpError226: (226, 'IM Used'),
      HttpError300: (300, 'Multiple Choices'),
      HttpError301: (301, 'Moved Permanently'),
      HttpError302: (302, 'Found'),
      HttpError303: (303, 'See Other'),
      HttpError304: (304, 'Not Modified'),
      HttpError305: (305, 'Use Proxy'),
      HttpError306: (306, 'Unused'),
      HttpError307: (307, 'Temporary Redirect'),
      HttpError400: (400, 'Bad Request'),
      HttpError401: (401, 'Unauthorized'),
      HttpError402: (402, 'Payment Required'),
      HttpError403: (403, 'Forbidden'),
      HttpError404: (404, 'Not Found'),
      HttpError405: (405, 'Method Not Allowed'),
      HttpError406: (406, 'Not Acceptable'),
      HttpError407: (407, 'Proxy Authentication Required'),
      HttpError408: (408, 'Request Timeout'),
      HttpError409: (409, 'Conflict'),
      HttpError410: (410, 'Gone'),
      HttpError411: (411, 'Length Required'),
      HttpError412: (412, 'Precondition Failed'),
      HttpError413: (413, 'Request Entity Too Large'),
      HttpError414: (414, 'Request-URI Too Long'),
      HttpError415: (415, 'Unsupported Media Type'),
      HttpError416: (416, 'Requested Range Not Satisfiable'),
      HttpError417: (417, 'Expectation Failed'),
      HttpError418: (418, 'Im a teapot'),
      HttpError422: (422, 'Unprocessable Entity'),
      HttpError423: (423, 'Locked'),
      HttpError424: (424, 'Failed Dependency'),
      HttpError425: (425, 'Unordered Collection'),
      HttpError426: (426, 'Upgrade Required'),
      HttpError500: (500, 'Internal Server Error'),
      HttpError501: (501, 'Not Implemented'),
      HttpError502: (502, 'Bad Gateway'),
      HttpError503: (503, 'Service Unavailable'),
      HttpError504: (504, 'Gateway Timeout'),
      HttpError505: (505, 'HTTP Version Not Supported'),
      HttpError506: (506, 'Variant Also Negotiates'),
      HttpError507: (507, 'Insufficient Storage'),
      HttpError510: (510, 'Not Extended')}
  
  # retrieves the status number and constant from the given exception class using the dictionary 
  try:
    (statuscode_numb, statuscode_constant) = httpstatuscode_dict[type(e)]
  except Exception, e:
    raise HttpServerError('Internal error on generating error msg: ' + str(e))

  # get any extra error msg that the callback fucntion raised 
  client_error_msg = str(e)

  # return what is retrieved
  return statuscode_numb, client_error_msg, statuscode_constant















"""
<Program Name>
  httpretrieve.repy

<Started>
  August 19, 2009

<Author>
  Yafete Yemuru

<Purpose>
  provides a http content from a web server using http protocol. It sends a http request to
  any http server through socket connection to get the http content. Then once the http server
  replies with http header and content, the http header is checked for any error message.
  Then provides http content in a format of string, saved in a file or as a file like object. 
"""




#begin include urlparse.repy  
"""
<Program Name>
  urlparse.repy

<Started>
  May 15, 2009

<Author>
  Michael Phan-Ba

<Purpose>
  Provides utilities for parsing URLs, based on the Python 2.6.1 module urlparse.

"""


def urlparse_urlsplit(urlstring, default_scheme="", allow_fragments=True):
  """
  <Purpose>
    Parse a URL into five components, returning a dictionary.  This corresponds
    to the general structure of a URL:
    scheme://netloc/path;parameters?query#fragment.  The parameters are not
    split from the URL and individual componenets are not separated.

    Only absolute server-based URIs are currently supported (all URLs will be
    parsed into the components listed, regardless of the scheme).

  <Arguments>
    default_scheme:
      Optional: defaults to the empty string.  If specified, gives the default
      addressing scheme, to be used only if the URL does not specify one.

    allow_fragments:
      Optional: defaults to True.  If False, fragment identifiers are not
      allowed, even if the URL's addressing scheme normally does support them.

  <Exceptions>
    ValueError on parsing a non-numeric port value.

  <Side Effects>
    None.

  <Returns>
    A dictionary containing:

    Key         Value                               Value if not present
    ============================================================================
    scheme      URL scheme specifier                empty string
    netloc      Network location part               empty string
    path        Hierarchical path                   empty string
    query       Query component                     empty string
    fragment    Fragment identifier                 empty string
    username    User name                           None
    password    Password                            None
    hostname    Host name (lower case)              None
    port        Port number as integer, if present  None

  """

  components = {"scheme": default_scheme, "netloc": "", "path": "", "query": "",
    "fragment": "", "username": None, "password": None, "hostname": None,
    "port": None }

  # Extract the scheme, if present.
  (lpart, rpart) = _urlparse_splitscheme(urlstring)
  if lpart:
    components["scheme"] = lpart

  # Extract the server information, if present.
  if rpart.startswith("//"):
    (lpart, rpart) = _urlparse_splitnetloc(rpart, 2)
    components["netloc"] = lpart

    (components["username"], components["password"], components["hostname"],
      components["port"]) = _urlparse_splitauthority(lpart)

  # Extract the fragment.
  if allow_fragments:
    (rpart, components["fragment"]) = _urlparse_splitfragment(rpart)


  # Extract the query.
  (components["path"], components["query"]) = _urlparse_splitquery(rpart)

  return components


def _urlparse_splitscheme(url):
  """Parse the scheme portion of the URL"""
  # The scheme is valid only if it contains these characters.
  scheme_chars = \
    "abcdefghijklmnopqrstuvwxyz0123456789+-."

  scheme = ""
  rest = url

  spart = url.split(":", 1)
  if len(spart) == 2:

    # Normalize the scheme.
    spart[0] = spart[0].lower()

    # A scheme is valid only if it starts with an alpha character.
    if spart[0] and spart[0][0].isalpha():
      for char in spart[0]:
        if char not in scheme_chars:
          break
      (scheme, rest) = spart

  return scheme, rest


def _urlparse_splitnetloc(url, start=0):
  """Parse the netloc portion of the URL"""

  # By default, the netloc is delimited by the end of the URL.
  delim = len(url)

  # Find the left-most delimiter.
  for char in "/?#":
    xdelim = url.find(char, start)
    if xdelim >= 0:
      delim = min(delim, xdelim)

  # Return the netloc and the rest of the URL.
  return url[start:delim], url[delim:]


def _urlparse_splitauthority(netloc):
  """Parse the authority portion of the netloc"""

  # The authority can have a userinfo portion delimited by "@".
  authority = netloc.split("@", 1)

  # Default values.
  username = None
  password = None
  hostname = None
  port = None

  # Is there a userinfo portion?
  if len(authority) == 2:

    # userinfo can be split into username:password
    userinfo = authority[0].split(":", 1)

    # hostport can be split into hostname:port
    hostport = authority[1].split(":", 1)

    if userinfo[0]:
      username = userinfo[0]
    if len(userinfo) == 2:
      password = userinfo[1]

  # No userinfo portion found.
  else:

    # hostport can be split into hostname:port
    hostport = netloc.split(":", 1)

  # Is there a port value?
  if hostport[0]:
    hostname = hostport[0]
  if len(hostport) == 2:
    port = int(hostport[1], 10)

  # Return the values.
  return username, password, hostname, port


def _urlparse_splitquery(url):
  """Parse the query portion of the url"""

  qpart = url.split("?", 1)
  if len(qpart) == 2:
    query = qpart[1]
  else:
    query = ""

  return qpart[0], query


def _urlparse_splitfragment(url):
  """Parse the query portion of the url"""

  fpart = url.split("#", 1)
  if len(fpart) == 2:
    fragment = fpart[1]
  else:
    fragment = ""

  return fpart[0], fragment

#end include urlparse.repy  
#begin include sockettimeout.repy
"""
<Description>
  Puts back in Python's non-blocking functionality.

  send():
    Raises SocketTimeout Error if the send call lasts
    longer than the set timeout.

  recv():
    Guarentees the receipt of a message.   Raises SocketTimeoutError if it does not
    receive any message before a given timeout.
    If actually receives the message, returns the message and continues.

<Usage>
  Text-replacable for Repy Sockets:
    timeout_openconn(desthost, destport, localip=None, localport=None, timeout = 5)
    timeout_waitforconn(localip, localport, function)

  Object:
    sockobj.settimeout(seconds)
    sockobj.send(data)
    sockobj.recv(bytes)
    sockobj.close()

<Date>
  Sun Mar  1 10:27:35 PST 2009

<Example>
  # hello world
  include sockettimer.repy

  def callback(ip, port, timeout_sockobj, commhandle, listenhandle):
    hw_message = timeout_sockobj.recv(1047)

    # cleanup
    stopcomm(commhandle)
    stopcomm(listenhandle)
    timeout_sockobj.close()

    print hw_message # => "hello world!"
  
  def server():
    sockobj = timeout_waitforconn(getmyip(), 12345, callback)

  def client():
    sockobj = timeout_openconn(getmyip(), 12345)
    sockobj.send("hello world!")

  def main():
    server()
    client()
    exitall()

  if callfunc == 'initialize':
    main() 
"""

class SocketTimeoutError(Exception):
  """The socket timed out before receiving a response"""

def timeout_openconn(desthost, destport, localip=None, localport=None, timeout = 5):
  """
  <Purpose> 
    Wrapper for Repy like socket interface

  <Args>
    Same as Repy openconn

  <Exception>
    Timeout exception if the dest address doesnt respond.

  <Returns>
    socket obj on success
  """

  tsock = TimeoutSocket()
  tsock.settimeout(timeout)
  if localip and localport:
    tsock.bind((localip, localport))
  tsock.connect((desthost, destport))
  return tsock

def timeout_waitforconn(localip, localport, function):
  """
  <Purpose> 
    Wrapper for Repy like socket interface

  <Args>
    Same as Repy waitforconn

  <Side Effects>
    Sets up event listener which calls function on messages.

  <Returns>
    Handle to listener.
  """

  tsock = TimeoutSocket()
  tsock.bind((localip, localport))
  tsock.setcallback(function)
  return tsock.listen()

class TimeoutSocket:
  """
  <Purpose>
    Provide an socket object like the Repy usual one.

  <Side Effects>
    Uses a getlock() to watch for a timeout
    Uses waitforconn and openconn to simulate socket
  """

  ################
  # Constructors
  ################

  def __init__(self):
    """ Constructor for socket """
#    self.lock = getlock() # general lock BUG: Do we need to lock everything?
    self.timeout_lock = getlock() # special lock for Timeout condition
    self.timeout = 5 # seconds to wait
    self.bytes_sent = None # used to check if send() timed out

    # user vars   
    self.local_address = None # ip, port
    self.remote_address = None # ip, port
    self.callback = None # the user's function to call

    # repy socket vars
    self.sockobj = None #  the Repy socket
    self.commhandle = None # the current comm
    self.listencommhandle = None # the listener comm

    #error tracking vars
    
    #if any exceptions are thrown in the separate thread executing _send_and_release, 
    #they are caught and stored in this variable, then raised in _send_or_close
    self.TCPSendError = None

  ################
  # Mutator methods
  #################

  def settimeout(self, value):
    """ Setter for timeout"""
    self.timeout = value

  def setcallback(self, function):
    """ Setter for callback function"""
    self.callback = function

  ####################
  # Public Methods
  ####################

  def bind(self, local_address = None):
    """
    <Purpose>
      Set local address

    <Args>
      Tuple of (ip, port) local.
    """
    self.local_address = local_address

  def listen(self):
    """
    <Purpose>
      Listen for peer
    
    <Side Effects>
      Calls Repy waitforconn()
    """
    return self._waitforconn()

  def connect(self, remote_address):
    """
    <Purpose>
      Connect to peer.

    <Args>
      Tuple of (ip, port) remote.
   
    <Side Effects>
      Calls Repy openconn.
    """
    self.remote_address = remote_address
    self._openconn()

  def recv(self, maxLen): # timeout as optional arg ???
    """
    <Purpose>
      If it fails to finish within the timeout, I close the socket and raise a
      TimeoutError exception. I.e. if there's no message, we call it an error
      and raise it.
      
    <Arguments>
      maxLen - bytes to recv

    <Exception>
      Raises TimeoutError exception if the recv times out
      without receiving a message.

    <Side Effects>
      Closes the connection if times out.

    <Returns>
      The message.
    """
    return self._recv_or_close(maxLen)

  def send(self, data):
    """
    <Purpose>
      Just like normal Repy socket.  Sends messages.
      
    <Arguments>
      data - the string message

    <Exception>
      Same as Repy socket.
 
    <Returns>
      The bytes sent.
    """
    return self._send_or_close(data)

  def close(self):
    self.local_address = None # ip, port
    self.remote_address = None # ip, port
    self.callback = None # the user's function to call

    if self.sockobj:
      self.sockobj.close()
    self.sockobj = None #  the Repy socket
    
    # Armon: As part of the semantics, stopcomm will raise an 
    # exception given an invalid handle, e.g. None. Thus,
    # we need to check for this.
    if self.commhandle: 
      stopcomm(self.commhandle)
      self.commhandle = None # the current comm
    
    # Armon: Same as above.
    if self.listencommhandle:
      stopcomm(self.listencommhandle)
      self.listencommhandle = None # the listener comm


  ########################
  # Private
  #########################

  def _openconn(self):
    """Handle current state variables and call Repy openconn."""

    destip, destport = self.remote_address
    if self.local_address:
      srcip, srcport = self.local_address
      self.sockobj = openconn(destip, destport, srcip, srcport, self.timeout)
    else:
      self.sockobj = openconn(destip, destport)

  def _waitforconn(self):
    """Setup way between Repy waitforconn event"""
    localip, localport = self.local_address
    self.listencommhandle = waitforconn(localip, localport, self._callback)
    return self.listencommhandle

  def _callback(self, ip, port, sockobj, ch, lh):
    """Pass on through to user callback"""
    self.sockobj = sockobj
    self.listencommhandle = lh # same as the 1st from wait for comm, right?
    self.commhandle = ch # should we care?
    
    if not self.remote_address:
      self.remote_address = (ip, port)
    else: 
      raise Exception("what! peer does not match?")

    self.callback(ip, port, self, ch, lh)

  def _send(self, data):
    """Send data"""
    return self.sockobj.send(data)

  def _recv(self, maxLen):
    """Recv data of length maxLen"""
    return self.sockobj.recv(maxLen)

  def _send_and_release(self, data):
    """Send data then release the timeout lock"""
    
    #Bug Fix (Cosmin): exceptions thrown in separate thread _send_and_release could not be caught
    #now we store the exception if it is thrown and raise it back in send_or_close
    try:
      self.bytes_sent = self._send(data)
    except Exception, e:
      self.TCPSendError = e
    
    self._quietly_release() # release the lock
 
  def _quietly_release(self):
    """Release the timeout lock and ignore if already released"""
    try:
      self.timeout_lock.release()
    except:
      pass
   
  def _send_or_close(self, data):
    """Raise the Timeout Error if no receipt.  Keep track by timeout_lock."""

    # acquire the lock, when it's release we'll carry on
    self.timeout_lock.acquire()

    # fork off a lock that'll release the lock at the timeout
    timerhandle = settimer(self.timeout, self._quietly_release, ())

    # fork off a send call so we can raise the exception in the main thread
    # the send call will also release our lock
    settimer(0, self._send_and_release, (data,))

    # block until either the timeout or _send finishes
    self.timeout_lock.acquire()
    self.timeout_lock.release()

    if self.bytes_sent: # send finished
      canceltimer(timerhandle)
      retdata = self.bytes_sent
      self.bytes_sent = None
      return retdata
    elif self.TCPSendError != None:
      #Bug Fix (Cosmin): exceptions thrown in separate thread _send_and_release could not be caught
      
      #we got an error within the separate thread that performed the send operation
      exception_to_throw = self.TCPSendError
      self.TCPSendError = None
      raise exception_to_throw
    else: # it timed out
      self.close()
      raise SocketTimeoutError

  def _recv_or_close(self, amount):
    """Raise the Timeout Error if no receipt.  Keep track by timeout_lock."""
    timerhandle = settimer(self.timeout, self._clobbersocket, ())
    try:
      retdata = self._recv(amount)
    except Exception, e:
      # if it's not the timeout, reraise...
      if self.timeout_lock.acquire(False):
        raise
      raise SocketTimeoutError
    
    # I acquired the lock, I should stop the timer because I succeeded...
    if self.timeout_lock.acquire(False):
      # even if this isn't in time, the lock prevents a race condition 
      # this is merely an optimization to prevent the timer from ever firing...
      canceltimer(timerhandle)
      self.timeout_lock.release() # Alper's bug 3/10/09
      return retdata
    else:
      raise SocketTimeoutError

  def _clobbersocket(self):
    """If I can acquire the lock without blocking, then close the socket to abort"""
    if self.timeout_lock.acquire(False):
      self.close()


############################
# Deprecated functions
##############################

# private function...
def sockettimeout_clobbersocket(sockobj,mylock):
  # if I can acquire the lock without blocking, then close the socket to abort
  if mylock.acquire(False):
    sockobj.close()

# if it fails to finish within the timeout, I close the socket and raise a
# SocketTimeout exception...
def sockettimeout_recv_or_close(sockobj, amount, timeout):
  # A lock I'll use for this attempt
  mylock = getlock()
  timerhandle = settimer(timeout,clobbersocket, (sockobj, mylock))
  try:
    retdata = sockobj.recv(amount)
  except Exception, e:
    # if it's not the timeout, reraise...
    if mylock.acquire(False):
      raise
    raise SocketTimeout
    
  # I acquired the lock, I should stop the timer because I succeeded...
  if mylock.acquire(False):
    # even if this isn't in time, the lock prevents a race condition 
    # this is merely an optimization to prevent the timer from ever firing...
    canceltimer(timerhandle)
    return retdata
  else:
    raise SocketTimeout


#end include sockettimeout.repy
#begin include http_hierarchy_error.repy
"""
<Program Name>
  http_hierarchy_error.repy

<Started>
  Oct 05, 2009

<Author>
  Yafete Yemuru

<Purpose>
  provides a hierachy http error using status code including client and server errors
  classes.  
"""


'''
http hierarchy error exception classes

-> HttpError
   -> HttpRetrieveClientError
      -> HttpUserInputError
      -> HttpConnectionError

   -> HttpServerError
      -> HttpResponseError
         -> HttpHeaderError
            -> HttpHeaderReceivingError
            -> HttpHeaderFormatError
         -> HttpContentError
            -> HttpContentReceivingError
            -> HttpContentLengthError
       
   -> HttpStatuscodeError
     -> HttpError1xx
        -> followed by all http status code error number HttpError(number)
        
     -> HttpError2xx
        -> followed by all http status code error number HttpError(number)
        
     -> HttpError3xx
        -> followed by all http status code error number HttpError(number)

     -> HttpError4xx
        -> followed by all http status code error number HttpError(number)
        
     -> HttpError5xx
        -> followed by all http status code error number HttpError(number)

'''

class HttpError(Exception):
  pass

# raises an exception for http client error 
class HttpRetrieveClientError(HttpError):# extend HttpError 
  pass
class HttpUserInputError(HttpRetrieveClientError):
  pass
class HttpConnectionError(HttpRetrieveClientError):
  pass


# raises an exception for any http server failure  
class HttpServerError(HttpError):# extend HttpError 
  pass
class HttpResponseError(HttpServerError):
  pass
class HttpHeaderError(HttpResponseError):
  pass
class HttpHeaderReceivingError(HttpHeaderError):
  pass
class HttpHeaderFormatError(HttpHeaderError):
  pass
class HttpContentError(HttpResponseError):
  pass
class HttpContentReceivingError(HttpContentError):
  pass
class HttpContentLengthError(HttpContentError):
  pass


class HttpStatusCodeError(HttpError):# extend HttpError
  pass
class HttpError1xx(HttpStatusCodeError):
  pass
class HttpError100(HttpError1xx):
  pass
class HttpError101(HttpError1xx): 
  pass
class HttpError102(HttpError1xx): 
  pass


class HttpError2xx(HttpStatusCodeError):
  pass
class HttpError201(HttpError2xx): 
  pass
class HttpError202(HttpError2xx):   
  pass
class HttpError203(HttpError2xx): 
  pass
class HttpError204(HttpError2xx): 
  pass
class HttpError205(HttpError2xx): 
  pass
class HttpError206(HttpError2xx): 
  pass
class HttpError207(HttpError2xx): 
  pass
class HttpError226(HttpError2xx): 
  pass                 


class HttpError3xx(HttpStatusCodeError):
  pass
class HttpError300(HttpError3xx): 
  pass
class HttpError301(HttpError3xx): 
  pass
class HttpError302(HttpError3xx): 
  pass
class HttpError303(HttpError3xx): 
  pass
class HttpError304(HttpError3xx):
  pass
class HttpError305(HttpError3xx): 
  pass
class HttpError306(HttpError3xx): 
  pass
class HttpError307(HttpError3xx): 
  pass
                    

class HttpError4xx(HttpStatusCodeError):
  pass
class HttpError400(HttpError4xx):
  pass  
class HttpError401(HttpError4xx): 
  pass
class HttpError402(HttpError4xx): 
  pass
class HttpError403(HttpError4xx):
  pass  
class HttpError404(HttpError4xx): 
  pass
class HttpError405(HttpError4xx): 
  pass
class HttpError406(HttpError4xx): 
  pass
class HttpError407(HttpError4xx): 
  pass
class HttpError408(HttpError4xx): 
  pass
class HttpError409(HttpError4xx): 
  pass
class HttpError410(HttpError4xx): 
  pass
class HttpError411(HttpError4xx): 
  pass
class HttpError412(HttpError4xx): 
  pass
class HttpError413(HttpError4xx): 
  pass
class HttpError414(HttpError4xx): 
  pass
class HttpError415(HttpError4xx): 
  pass
class HttpError416(HttpError4xx): 
  pass
class HttpError417(HttpError4xx): 
  pass
class HttpError418(HttpError4xx): 
  pass
class HttpError422(HttpError4xx): 
  pass
class HttpError423(HttpError4xx): 
  pass
class HttpError424(HttpError4xx): 
  pass
class HttpError425(HttpError4xx): 
  pass
class HttpError426(HttpError4xx): 
  pass


class HttpError5xx(HttpStatusCodeError):
  pass
class HttpError500(HttpError5xx): 
  pass
class HttpError501(HttpError5xx): 
  pass
class HttpError502(HttpError5xx): 
  pass
class HttpError503(HttpError5xx): 
  pass
class HttpError504(HttpError5xx): 
  pass
class HttpError505(HttpError5xx): 
  pass
class HttpError506(HttpError5xx):
  pass  
class HttpError507(HttpError5xx):
  pass  
class HttpError510(HttpError5xx):
  pass

#end include http_hierarchy_error.repy
#begin include urllib.repy
def urllib_quote(string, safe="/"):
  """
  <Purpose>
    Encode a string such that it can be used safely in a URL or XML
    document.

  <Arguments>
    string:
           The string to urlencode.

    safe (optional):
           Specifies additional characters that should not be quoted --
           defaults to "/".

  <Exceptions>
    TypeError if the safe parameter isn't an enumerable.

  <Side Effects>
    None.

  <Returns>
    Urlencoded version of the passed string.
  """

  resultstr = ""

  # We go through each character in the string; if it's not in [0-9a-zA-Z]
  # we wrap it.

  safeset = set(safe)

  for char in string:
    asciicode = ord(char)
    if (asciicode >= ord("0") and asciicode <= ord("9")) or \
        (asciicode >= ord("A") and asciicode <= ord("Z")) or \
        (asciicode >= ord("a") and asciicode <= ord("z")) or \
        asciicode == ord("_") or asciicode == ord(".") or \
        asciicode == ord("-") or char in safeset:
      resultstr += char
    else:
      resultstr += "%%%02X" % asciicode

  return resultstr




def urllib_quote_plus(string, safe=""):
  """
  <Purpose>
    Encode a string to go in the query fragment of a URL.

  <Arguments>
    string:
           The string to urlencode.

    safe (optional):
           Specifies additional characters that should not be quoted --
           defaults to the empty string.

  <Exceptions>
    TypeError if the safe parameter isn't a string.

  <Side Effects>
    None.

  <Returns>
    Urlencoded version of the passed string.
  """

  return urllib_quote(string, safe + " ").replace(" ", "+")




def urllib_unquote(string):
  """
  <Purpose>
    Unquote a urlencoded string.

  <Arguments>
    string:
           The string to unquote.

  <Exceptions>
    ValueError thrown if the last wrapped octet isn't a valid wrapped octet
    (i.e. if the string ends in "%" or "%x" rather than "%xx". Also throws
    ValueError if the nibbles aren't valid hex digits.

  <Side Effects>
    None.

  <Returns>
    The decoded string.
  """

  resultstr = ""

  # We go through the string from end to beginning, looking for wrapped
  # octets. When one is found we add it (unwrapped) and the following
  # string to the resultant string, and shorten the original string.

  while True:
    lastpercentlocation = string.rfind("%")
    if lastpercentlocation < 0:
      break

    wrappedoctetstr = string[lastpercentlocation+1:lastpercentlocation+3]
    if len(wrappedoctetstr) != 2:
      raise ValueError("Quoted string is poorly formed")

    resultstr = \
        chr(int(wrappedoctetstr, 16)) + \
        string[lastpercentlocation+3:] + \
        resultstr
    string = string[:lastpercentlocation]

  resultstr = string + resultstr
  return resultstr




def urllib_unquote_plus(string):
  """
  <Purpose>
    Unquote the urlencoded query fragment of a URL.

  <Arguments>
    string:
           The string to unquote.

  <Exceptions>
    ValueError thrown if the last wrapped octet isn't a valid wrapped octet
    (i.e. if the string ends in "%" or "%x" rather than "%xx". Also throws
    ValueError if the nibbles aren't valid hex digits.

  <Side Effects>
    None.

  <Returns>
    The decoded string.
  """

  return urllib_unquote(string.replace("+", " "))




def urllib_quote_parameters(dictionary):
  """
  <Purpose>
    Encode a dictionary of (key, value) pairs into an HTTP query string or
    POST body (same form).

  <Arguments>
    dictionary:
           The dictionary to quote.

  <Exceptions>
    None.

  <Side Effects>
    None.

  <Returns>
    The quoted dictionary.
  """

  quoted_keyvals = []
  for key, val in dictionary.items():
    quoted_keyvals.append("%s=%s" % (urllib_quote(key), urllib_quote(val)))

  return "&".join(quoted_keyvals)




def urllib_unquote_parameters(string):
  """
  <Purpose>
    Decode a urlencoded query string or POST body.

  <Arguments>
    string:
           The string to decode.

  <Exceptions>
    ValueError if the string is poorly formed.

  <Side Effects>
    None.

  <Returns>
    A dictionary mapping keys to values.
  """

  keyvalpairs = string.split("&")
  res = {}

  for quotedkeyval in keyvalpairs:
    # Throw ValueError if there is more or less than one '='.
    quotedkey, quotedval = quotedkeyval.split("=")
    key = urllib_unquote(quotedkey)
    val = urllib_unquote(quotedval)
    res[key] = val

  return res

#end include urllib.repy





def httpretrieve_open(url, http_query=None, http_post=None, http_header=None, header_timeout=30, content_timeout=30, httpheader_limit=8192, httpcontent_limit=4194304):
  """
  <Purpose>
     Returns file like object that that can read the http content form a http server. The file like
     object gets string from http server using read method.  

  <Arguments>
    url:
           String of a http web server-URL
    http_post:
           dictionary of data to post to server(unencoded string, the library encodes the post it self)
    http_query:
           dictionary of query to send to server(unencoded string, the library encodes the query it self)
    http_header:
           dictionary of http header to add the the http header request
    header_timeout:
           socket timeout for receiving header from server(default value set to 30 seconds)
    content_timeout:
           socket timeout for receiving content from server(default value set to 30 seconds)
    httpheader_limit:
           length limit for when a server sends http header(default value set to 8kb(8192 charactors)) 
    httpcontent_limit:
            limits the the amount of content a server can send to the retrieval 
 
  <Exceptions>
        HttpUserInputError
            ->  If given a invalid URL 
            ->  If given a none http protocol server
            ->  if file like object read is given a negative number or a none int as a limit
            ->  if the file like object is called after it is closed

        HttpConnectionError
            ->  if opening connection with server fails      
            ->  if sending http request to http server fails  

        HttpHeaderReceivingError
            ->  If the timeout(default timeout set to 5 seconds) for receiving exceeds   
            ->  If the http header length exceeds (default 
            
        HttpHeaderFormatError
            ->  If The http header is too long(default set to 8 kb(8192 charactors))
            ->  If the http header statuscode format is invalid. The right http header
                    status code includes HTTP<version> http_status_number http_status_msg                 
            ->  If the http server gives a http header with a invalid content length
                    or invalid redirect location
            
        HttpContentReceivingError:
            ->  if the http server fails to send http content 
            ->  if the timeout(default timeout set to 5 seconds) for receiving exceeds
            ->  if the server socket connection fails for any reason besides connection closing
                    during receiving http content
                        
        HttpContentLengthError:
            ->  if content length exceeds(default set to 4096 kb(4194304 charactors)) 
                    (ONLY WORKS CONTENT LENGTH IS GIVEN BY THE HTTP SERVER)
            ->  If the total received length is not the same as the content length(this check will fail
                     if the content length isnt given)
            ->  If read is called with limits and it returns a empty string but the total read is                                      
                     not equal to the content length(this check will fail if the content length isnt given)                
                                            
        HttpStatuscodeError:
            -> if the http response status code isnt ok or redirect, it will raise an exception
                   depending up on the http protocol status number  
        

  <Side Effects>
    None 

  <Returns>
    Returns file like obj which can read the http content from http web server. 
  """
  
  # check if url is valid and get host, path, port and query from the given url
  (host, port, path, url_query) = _httpretrieve_parse_given_url(url)

  # get connection to the http web server
  try:
    sock = timeout_openconn(host, port)
    
  except Exception, e:
    raise HttpConnectionError('Error: opening a connection failed with given http server, Given: ' + str(url) + ' ' + str(e))
    
  # build a http format request using the given port, host, path and query
  httpheader = _httpretrieve_buildhttprequest(http_header, port, host, path, url_query, http_query, http_post)
  
  # send http format request to http web server  
  _httpretrieve_sendhttprequest(sock, httpheader) 
  
  # receive the http header lines in a form of list from the http web server
  httpheaderlines = _httpretrieve_receive_httpheader(sock, header_timeout, httpheader_limit)
  
  # get the http status number and http status msg from http header response
  (http_status_number, http_status_msg) = _httpretrieve_get_httpstatuscode(httpheaderlines)

  if http_status_number == '200':# ok message
    # gets the content length if given.
    contentlength = _httpretrieve_get_contentlength(httpheaderlines)
    # return a filelikeobj to read the http content from the http server 
    return _httpretrieve_filelikeobject(sock, contentlength, httpcontent_limit, content_timeout) 
  
  elif http_status_number == '301' or http_status_number == '302': # redirect
    # redirect to the new location via recursion  
    sock.close()
    # get the redirection location
    redirect_location = _httpretrieve_httpredirect(httpheaderlines) 
    # redirect to the new location using recursion
    return httpretrieve_open(redirect_location)     

  else:
    # if given receive content length inorder to check http content error is received fully
    contentlength = _httpretrieve_get_contentlength(httpheaderlines)
    # receive the http content error 
    http_errorcontent = _httpretrieve_receive_httperror_content(sock, contentlength)
    # raise exception depending up on the http status number and add on the http error content after a
    # discription that says 'Http error content: '
    _httpretrieve_raise_httpstatuscode_error(http_status_number, http_status_msg, http_errorcontent)   


  


def httpretrieve_save_file(url, filename, http_query=None, http_post=None, http_header=None, header_timeout=30, content_timeout=30, httpheader_limit=8192, httpcontent_limit=4194304):
  """
  <Purpose>
     Saves http content of the given URL to current directory  

  <Arguments>
    url:
           String of a http web server URL
    filename:
           The file name for the http content to be saved in
    http_post:
           dictionary of data to post to server(unencoded string, the library encodes the post it self)
    http_query:
           dictionary of query to send to server(unencoded string, the library encodes the query it self)
    http_header:
           dictionary of http header to add the the http header request
    header_timeout:
           socket timeout for receiving header from server(default value set to 30 seconds)
    content_timeout:
           socket timeout for receiving content from server(default value set to 30 seconds)
    httpheader_limit:
           length limit for when a server sends http header(default value set to 8kb(8192 charactors)) 
    httpcontent_limit:
            limits the the amount of content a server can send to the retrieval 
           
  <Exceptions>
  
    HttpRetrieveClientError: cant create a file to save the http content too
    Also includes:  all the exception from httpretrieve_open 

  <Side Effects>
    same as httpretrieve_open  

  <Returns>
    None 
  """
  
  httpcontent = ''
  try:
    # create a new file with the given filename
    newfile = open(filename, 'w')
  except Exception, e:
    raise HttpRetrieveClientError('Error on creating a file to saving http content' + str(e))

  http_obj = httpretrieve_open(url, http_query, http_post, http_header, header_timeout, content_timeout, httpheader_limit, httpcontent_limit)

  # keep on reading 1024 and writing it into a file, until it receives an empty string
  # which means the http server content is completely read 
  while True:
    httpcontent = http_obj.read(1024)
    if httpcontent == '':
      # done reading close file and file like obj and exit loop 
      newfile.close()  
      http_obj.close()
      break
    newfile.write(httpcontent)


  
def httpretrieve_get_string(url, http_query=None, http_post=None, http_header=None, header_timeout=30, content_timeout=30, httpheader_limit=8192, httpcontent_limit=4194304):
  """
  <Purpose>
     retruns string of the http content from a given URL

  <Arguments>
    url:
           String of a http web server-URL
    http_post:
           dictionary of data to post to server(unencoded string, the library encodes the post it self)
    http_query:
           dictionary of query to send to server(unencoded string, the library encodes the query it self)
    http_header:
           dictionary of http header to add the the http header request
    header_timeout:
           socket timeout for receiving header from server(default value set to 30 seconds)
    content_timeout:
           socket timeout for receiving content from server(default value set to 30 seconds)
    httpheader_limit:
           length limit for when a server sends http header(default value set to 8kb(8192 charactors)) 
    httpcontent_limit:
            limits the the amount of content a server can send to the retrieval 
 
  <Exceptions>
     same as httpretrieve_open

  <Side Effects>
     same as httpretrieve_open 

  <Returns>
     returns a string of the http content. 
  """       
  
  http_obj = httpretrieve_open(url, http_query, http_post, http_header, header_timeout, content_timeout, httpheader_limit, httpcontent_limit)
  # retrieve the http content from server using httpretrieve file like object
  httpcontent = http_obj.read()
  http_obj.close()
  # return the http content in a form of string
  return httpcontent



class _httpretrieve_filelikeobject:
  # file like object used to receive the http content with a length limit   
  def __init__(self, sock, contentlength, httpcontent_limit, content_timeout):
    self.sock = sock
    if contentlength == None:
      self.contentlengthisknown = False
    else:
      self.contentlengthisknown = True
      self.contentlength = contentlength
    self.httpcontent_limit = httpcontent_limit  
    self.content_timeout = content_timeout  
    self.fileobjclosed = False
    self.totalcontentisreceived = False 
    self.totalread = 0
    

  def read(self, limit = None):
    """
    <Purpose>
        reads the http content from http server using the file like object   

    <Arguments>
        limit(optional):
             maximum number of bytes to read. If not specified the whole file is read.
             Can be 0 or any positive int
   
    <Exceptions>

        HttpContentReceivingError:
            ->  if the http server fails to send http content 
            ->  if the timeout(default timeout set to 5 seconds) for receiving exceeds
            ->  if the server socket connection fails for any reason besides connection closing
                    during receiving http content
        HttpContentLengthError:
            ->  if content length exceeds(default set to 4096 kb(4194304 charactors))
                    (ONLY WORKS CONTENT LENGTH IS GIVEN BY THE HTTP SERVER)
            ->  If the total received length is not the same as the content length(this check will fail
                     if the content length isnt given)
            ->  If read is called with limits and it returns a empty string but the total read is                                      
                     not equal to the content length(this check will fail if the content length isnt given)
                     
        HttpStatuscodeError:
            if the http response status code isnt ok or redirect, it will raise an exception
            depending up on the http protocol status number  


    <Side Effects>
       None


    <Returns>
      returns the content of http server in a form of string or an empty string if the content is completely read.
    """
    
    # raises an exception, if read is called after the filelikeobj is closed 
    if self.fileobjclosed == True:
      raise HttpUserInputError('Http Error: filelikeobj is closed')

    # if read is called after all http content received return an empty string
    if self.totalcontentisreceived:
      return ''
   
    # check if limit is given
    if limit == None: 
      readhaslimit = False 
      left_to_read = 1024
    else: 
    # check if limit is a valid number
      if not type(limit) == int:
        raise HttpUserInputError('User input Error: given a none int to receive' + str(e))  
      elif limit < 0:
        # raise an exception if limit is a negative number
        raise HttpUserInputError('User input Error: given a negative number to receive, given: ' + str(limit))
      readhaslimit = True
      left_to_read = limit  

    # set a timeout for receiveing content from server 
    self.sock.settimeout(self.content_timeout)

    # if limit is given it will receiveby subtracting what is left until the limit is reached 
    # if limit isnt given it will receive1024 until the server closes connection       
    httpcontent = ''
    while True:
      try:
        content = self.sock.recv(left_to_read)

      except SocketTimeoutError:
        # raise an exception if receiveis taking too long to respond
        self.sock.close()  
        raise HttpContentReceivingError('Timeout Error on receiving content: server taking too long to send content')  

      except Exception , e:
        # socket closed - signal for when the server is done sending content
        # if there is any other exceptions close connection and raise an error  
        if 'Socket closed' not in str(e): 
          self.sock.close()            
          raise HttpContentReceivingError('Error on receiving content:' + str(e))
        self.totalcontentisreceived = True
        break

      else:
        # By default, httpretrieve permits content length to be less than 4,096 kilobytes(4194304 charactors)
        if len(content) >= self.httpcontent_limit:
          raise HttpContentLengthError('content length exceeded ' + self.httpcontent_limit)

        # add what is received
        httpcontent += content
        if readhaslimit:
          # keep subtracting what is left to receieve until it reachs the given limit amount
          self.totalread += len(content)
          if len(content) == left_to_read:
            break
          else:
            left_to_read -= len(content)

    # check if there was an error during reciving http content
    self._check_recieving_error(readhaslimit, httpcontent)

    return httpcontent
  

  def close(self):
    """
    <Purpose>
      close the file like object 

    <Arguments>
      None
   
    <Exceptions>
      None 

    <Side Effects>
      closes socket connection for the http client to http server

    <Returns>
      Nothing 
    """   
    self.fileobjclosed = True# flag used to raise an exception if the file like object is called after closed
    self.sock.close()


  def _check_recieving_error(self, readhaslimit, httpcontent):
    if len(httpcontent) == 0:
      self.sock.close()
      raise HttpContentLengthError('Error on recieving content: received a http header but didnt receive any http content')
    
    if self.contentlengthisknown:                    
      # if limit is given and content length is given and total content is received, check the total read equals the content length    
      if readhaslimit and self.totalcontentisreceived:
        if self.totalread != self.contentlength:
          self.sock.close()                
          raise HttpContentLengthError('Total length read with limit did not match the content length: total read: ' + str(self.totalread) + ' content length: ' + str(self.contentlength))

      # if called read without limit and content length is given; check if the received length is the same as the content length       
      if readhaslimit == False:
        if len(httpcontent) != self.contentlength:
          self.sock.close()
          raise HttpContentLengthError('Total received length did not match the content length: received: ' + str(len(httpcontent)) + ' content length : ' + str(self.contentlength))     





def _httpretrieve_parse_given_url(url):
  # checks if the URL is in the right format and returns a string of host, port, path and query by parsing the URL  
  try:
   # returns a dictionary of {scheme, netloc, path, quer, fragment, username, password, hostname and port} form the url                     
    urlparse = urlparse_urlsplit(url)  
  except Exception, e:
    raise HttpUserInputError('Given URL error: ' + str(e))
  else:
    # check if the protocol is http 
    if urlparse['scheme'] != 'http':
      raise HttpUserInputError('Given URL error: the given protocol ' + urlparse['scheme'] + ' isnt supported')       
    if urlparse['hostname'] == None:
      raise HttpUserInputError('Given URL error: host name is not given') 

    # get only the host path, port, query from the urlparse dictionary
    host = urlparse['hostname']
    path = urlparse['path']
    query = urlparse['query']
    
    # use default port 80 if the port isnt given                    
    if urlparse['port'] == None:
      port = 80 
    else:
      port = urlparse['port']

    return host, port, path, query





def _httpretrieve_buildhttprequest(http_header, port, host, path, url_query, dict_query, http_post):
  # send http request to the http web server using socket connection  
  
  if http_post != None:
    # there is a posted data, thus use http POST command
   
    # check if the given post data is valid
    if not type(http_post) == dict:
      raise HttpUserInputError('The given http_post is not a dictionary, given: ' + str(type(http_post)))

    # change the given http post dictionary into a encoded post data with a key and val  
    try: 
      http_post = urllib_quote_parameters(http_post)
    except Exception, e:
      raise HttpUserInputError('Error encoding the given http post dictionary ' +  str(http_post) + str(e))


    # build the main http request header which includes the GET/POST and the Host name field
    httpheader = _httpretrieve_httprequestmain_header('POST', url_query, dict_query, path, host, port)

    # if given add a client http header to the request
    httpheader += _httpretrieve_parse_clienthttpheader(http_header)

    # indicate the http post content length
    httpheader += 'Content-Length: ' + str(len(http_post)) + '\r\n'  
    # add a new line to indicate that the http header is done and the http post is followed.
    httpheader += '\r\n'
    # include the posted data after the http header empty line
    httpheader += http_post
        

  else:
    # there is no posted data, use http GET method   
    httpheader = _httpretrieve_httprequestmain_header('GET', url_query, dict_query, path, host, port)
    # if http header is given, add client headers to the request 
    httpheader += _httpretrieve_parse_clienthttpheader(http_header)
    # add a new line to indicate that the header request is complete
    httpheader += '\r\n'

  # return header with a new line which is signal for http header is done 
  return httpheader 




def _httpretrieve_httprequestmain_header(http_command, url_query, dict_query, path, host, port):
  # builds the first two main http request headers which include the GET/POST and the HOST name
  
  # before building the httprequest make sure there isnt two fields of query given by the client
  if url_query != '' and dict_query != None:
    # cant have two different fields with query
    raise HttpUserInputError('Cant input a http query with the url and an extra parameter dictionary with a http query')

  elif dict_query != None:
    # user has given a http query 
    try: 
      encoded_query = '?' + urllib_quote_parameters(dict_query)
    except Exception, e:
      raise HttpUserInputError('Error encoding the given http query dictionary ' +  str(dict_query) + str(e))

  elif url_query != '':
    # if there is a query include the query on the main header('?' is used as a seperater between path)
    encoded_query = '?' + url_query
  else:
    # there is no query
    encoded_query = ''
    

  # if there is no path add a '/' on the request and if there is a path use the given path
  addpath = '/'
  if path != '':
    addpath = path

  # FIRST header which includes the POST/GET request  
  main_httpheader = http_command + ' ' + addpath + encoded_query + ' HTTP/1.0\r\n'


  # if port is 80, dont need to include the port upon request
  addport = ''
  if port != 80:
    # if the port is not 80 the host needs to include the port number on Host header
    # (':' is used as a separater between host and port)
    addport = ':' + str(port)

  # SECOND line of the header request which include the host name with port if the port is not 80   
  main_httpheader += 'Host: ' + host + addport + '\r\n'

  # return the firs two lines of the http request 
  return main_httpheader




def _httpretrieve_parse_clienthttpheader(http_header):
  # builds a http header from the given http header dictionary
  if http_header == None:
    # if the http header isnt given return a empty string
    return ''
  elif not type(http_header) == dict:
    # raise an exception if the http header isnt dictionary
    raise HttpUserInputError('The given http header is not a dictionary, given: ' + str(type(http_header)))
  else: 
    # take the given key and val from the http_header dictionary and add them to the http header with
    # correct http format
    clienthttpheader = ''
    for key, val in http_header.items():
      # make simple checks on the key and val 
      if not type(key) == str:
        raise HttpUserInputError('The given http header key isnt str given ' + str(type(key)))
      if not type(val) == str:
        raise HttpUserInputError('The given http header value isnt str given ' + str( type(val)))
      if key == '' or val == '':
        # raise an exception if the key or value is a empty field
        raise HttpUserInputError('The given empty http header feild of key or value')
      if key.capitalize() != key:
        raise HttpUserInputError('The given http header key is not capitalized, given: ' + key)

      # add the key and value to the http header field
      clienthttpheader += key + ' : ' + val + '\r\n'  

    # return the string of the http header  
    return clienthttpheader




def _httpretrieve_sendhttprequest(sock, httpheader):
  # send the request, and if there is any error raise an excetion
  try:
    sock.send(httpheader)
  except Exception, e:
    if 'Socket closed' not in str(e): 
      sock.close()
    raise HttpConnectionError('Connection error: on sending http request to server ' + str(e))



  
def _httpretrieve_receive_httpheader(sock, header_timeout, httpheader_limit):
  # receives the http header leaving alone rest of the http response and returns in list
  # of each header as a line. default httpheader limit is set to 8 kb                        

  # set a time out if the server fails to send http header 
  sock.settimeout(header_timeout)

  httpheader_received = 0 
  httpheader = '' 
  while True:
    # receive until a empty line (\n\n or \r\n\r\n ) which separates the
    # http header from the http content
    if '\r\n\r\n' in httpheader:
      # return split to return a list of httpheader lines
      return httpheader.split('\r\n')
    if '\n\n' in httpheader:
      # return split to return a list of httpheader lines
      return httpheader.split('\n')

    if httpheader_limit == httpheader_received:
      sock.close()                  
      raise HttpHeaderFormatError('Http header length Error: The http header is too long, exceeded 8 kb')
                        
    try:
      # receive one character at a time inorder to check for the empty line
      content = sock.recv(1)
      # keep track of the received characters to raise an exception if the limit is exceeded                  
      httpheader_received += 1                  

    except SocketTimeoutError:
      raise HttpHeaderReceivingError('Timeout Error on receiving header: server taking too long to send http header')
    except Exception, e:
      sock.close() 
      raise HttpHeaderReceivingError('Error on recieving http header: ' + str(e))
    else:
      # if there was not receiving error add keep on adding the receieved content
      httpheader += content




def _httpretrieve_get_httpstatuscode(httpHeaderLines): 
  # checks if the http status code is valid and return the status number and msg 

  # http response header includes 3 "words": HTTP<version> http_status_number http_status_msg 
  httpstatusheader = httpHeaderLines[0]
  headersplit = httpstatusheader.split(' ', 2)

  # length of the header has to be 3 or greater because depending up on the http_status_msg might be more than one word
  if len(headersplit) != 3:
    raise HttpHeaderFormatError('Invalid Http header status code format: Correct format is HTTP<version> http_status_number http_status_msg: Given '  + httpstatusheader)
  if not httpstatusheader.startswith('HTTP'):
    raise HttpHeaderFormatError('Invalid Http header status code format: Http header status code should start of with HTTP<version> but given: '  + httpstatusheader)

  # the first split is the http version
  http_version = headersplit[0]                      

  # check if http_status_number is valid int
  try: 
    int(headersplit[1])
  except ValueError, e:
    raise HttpHeaderFormatError('Invalid Http header status code format: Status number should be a int, Given: ' + str(headersplit[1]) + str(e))
  else:
    http_status_number = headersplit[1]
  
  # what ever is left is the http status msg
  http_status_msg = headersplit[2]
  
  # return the values
  return http_status_number, http_status_msg




def _httpretrieve_receive_httperror_content(sock, contentlength):
  # receives the http error content which is located after the http error header                        
  httperror_content = '' 
  while True:
    try:
      content = sock.recv(1024)                  

    except SocketTimeoutError:
      raise HttpContentReceivingError('Timeout Error on receiving http error conent: server taking too long to send http error content')
    except Exception, e:
      # socket closed - signal for when the server is done sending error content
      # if there is any other exceptions close connection and raise an error besides socket closing  
      if 'Socket closed' not in str(e): 
        sock.close()            
        raise HttpContentReceivingError('Error on receiving http error content: ' + str(e))
      break
        
    else:
      # if there was not a receiving error keep on adding the receieved content
      httperror_content += content

  # return the received http error content. If the content length is given check
  # if the content length maches the received content
  if contentlength != None:
    if contentlength != len(httperror_content):
      raise HttpContentLengthError('Error on receiving http error content: received conent length: ' + str(len(httperror_content)) + ' actual content length: ' + str(contentlength))   
  return httperror_content      



    
def _httpretrieve_raise_httpstatuscode_error(http_status_number, http_status_msg, http_errorcontent): 
  # raises an exception using the http_status_number 1xx for Informational, 2xx for Success 3xx for Redirection,
  # 4xx for Client Error, and 5xx Server Error
 
  # raise a detailed error message explaining the http_status_number and http_status_msg for popular http errors  
  if http_status_number == '202':
    raise HttpError202('Http response error: ' + http_status_number + ' ' + http_status_msg +  ' http proccesing not responding. Http error content: ' + http_errorcontent)      
  elif http_status_number == '204':
    raise HttpError204('Http response error: ' + http_status_number + ' ' + http_status_msg +  ' thier is no http body content. Http error content: ' + http_errorcontent) 
  elif http_status_number == '300':
    raise HttpError300('Http response error: ' + http_status_number + ' ' + http_status_msg +  ' multiple redirect isnt suported. Http error content: ' + http_errorcontent)                
  elif http_status_number == '404':
    raise HttpError404('Http response error: ' + http_status_number + ' ' + http_status_msg +  ' cant find anything matching the given url. Http error content: ' + http_errorcontent)                
  elif http_status_number == '403':
    raise HttpError403('Http response error: ' + http_status_number + ' ' + http_status_msg +  ' the request was illegal. Http error content: ' + http_errorcontent)                
  elif http_status_number == '400':
    raise HttpError400('Http response error: ' + http_status_number + ' ' + http_status_msg +  ' the request contians bad syntex. Http error content: ' + http_errorcontent)                
  elif http_status_number == '500':
    raise HttpError500('Http response error: ' + http_status_number + ' ' + http_status_msg +  ' The server encountered an unexpected condition. Http error content: ' + http_errorcontent)                 
  elif http_status_number == '502':
    raise HttpError502('Http response error: ' + http_status_number + ' ' + http_status_msg +  ' acting like a gateway received an invalid response. Http error content: ' + http_errorcontent)                

  # if the http number wasnt any of the popular http error msgs, raise an exception using
  # the defualt http status number with http status msg  
  elif http_status_number >= '100' and http_status_number < '200': 
    raise HttpError1xx('Http response error: Information ' + http_status_number + ' ' + http_status_msg + '.Http error content: ' + http_errorcontent) 
  elif http_status_number > '200' and http_status_number < '300': 
    raise HttpError2xx('Http response error: success error ' + http_status_number + ' ' + http_status_msg + '.Http error content: ' + http_errorcontent)
  elif http_status_number >= '300' and http_status_number < '400': 
    raise HttpError3xx('Http response error: Redirection error' + http_status_number + ' ' + http_status_msg + '.Http error content: ' + http_errorcontent)
  elif http_status_number >= '400' and http_status_number < '500': 
    raise HttpError4xx('Http response error: client error ' + http_status_number + ' ' + http_status_msg + '.Http error content: ' + http_errorcontent)  
  elif http_status_number >= '500' and http_status_number < '600': 
    raise HttpError5xx('Http response error: server error: ' + http_status_number + ' ' + http_status_msg + '.Http error content: ' + http_errorcontent)
  else:
    raise HttpStatusCodeError('Http response error: invalid http status response, given ' + http_status_number + '.Http error content: ' + http_errorcontent)  




def _httpretrieve_httpredirect(httpheaderlines):
  # given http header retruns the redirect location   

  # if there is a redirect location given by the server it will look like
  # eg.'Location: http://www.google.com'
  for headerline in httpheaderlines:
    if headerline.startswith('Location:'):
      # if found redirect need to strip out 'Location: ' to return the url   
      redirect = headerline[len('Location: '):]
                        
      # check if the redirect has given a location then return it
      if len(redirect) == 0:
        raise HttpHeaderFormatError('Http header redirection format error: http server gave a redierect location with no URL')
      return redirect
                        
  # there wasn't a redirect location given
  raise HttpHeaderFormatError('Http header redirection format error: http redirect header didnt include the location')  




def _httpretrieve_get_contentlength(httpheaderlines):
  # returns the content legth if given or returns None if not given by server

  # if there is a content length given by the server it will look like
  # eg.'Content-Length: 34'
  for headerline in httpheaderlines:
    if headerline.startswith('Content-Length:'):
      # if found content length need to strip out 'Content-Length: ' to return the length   
      
      try: 
        contentlength = int(headerline[len('Content-Length: '):])
      except ValueError, e:
        raise HttpHeaderFormatError('Http header Content-Length format error: http server provided content length that isnt a int ' + str(e))                

      
      # check if the content length is valid and retrun it 
      if contentlength <= 0:                
        raise HttpHeaderFormatError('Http header Content-Length format error: provided content length with invalid number ' + str(contentlength))
      else:
        return contentlength
                        
  # there wasn't a content-length line or the content length was given but didnt give a int 
  return None




  
def urllib_quote(string, safe="/"):
  """
  <Purpose>
    Encode a string such that it can be used safely in a URL or XML
    document.

  <Arguments>
    string:
           The string to urlencode.

    safe (optional):
           Specifies additional characters that should not be quoted --
           defaults to "/".

  <Exceptions>
    TypeError if the safe parameter isn't an enumerable.

  <Side Effects>
    None.

  <Returns>
    Urlencoded version of the passed string.
  """

  resultstr = ""

  # We go through each character in the string; if it's not in [0-9a-zA-Z]
  # we wrap it.

  safeset = set(safe)

  for char in string:
    asciicode = ord(char)
    if (asciicode >= ord("0") and asciicode <= ord("9")) or \
        (asciicode >= ord("A") and asciicode <= ord("Z")) or \
        (asciicode >= ord("a") and asciicode <= ord("z")) or \
        asciicode == ord("_") or asciicode == ord(".") or \
        asciicode == ord("-") or char in safeset:
      resultstr += char
    else:
      resultstr += "%%%02X" % asciicode

  return resultstr




def urllib_quote_plus(string, safe=""):
  """
  <Purpose>
    Encode a string to go in the query fragment of a URL.

  <Arguments>
    string:
           The string to urlencode.

    safe (optional):
           Specifies additional characters that should not be quoted --
           defaults to the empty string.

  <Exceptions>
    TypeError if the safe parameter isn't a string.

  <Side Effects>
    None.

  <Returns>
    Urlencoded version of the passed string.
  """

  return urllib_quote(string, safe + " ").replace(" ", "+")




def urllib_unquote(string):
  """
  <Purpose>
    Unquote a urlencoded string.

  <Arguments>
    string:
           The string to unquote.

  <Exceptions>
    ValueError thrown if the last wrapped octet isn't a valid wrapped octet
    (i.e. if the string ends in "%" or "%x" rather than "%xx". Also throws
    ValueError if the nibbles aren't valid hex digits.

  <Side Effects>
    None.

  <Returns>
    The decoded string.
  """

  resultstr = ""

  # We go through the string from end to beginning, looking for wrapped
  # octets. When one is found we add it (unwrapped) and the following
  # string to the resultant string, and shorten the original string.

  while True:
    lastpercentlocation = string.rfind("%")
    if lastpercentlocation < 0:
      break

    wrappedoctetstr = string[lastpercentlocation+1:lastpercentlocation+3]
    if len(wrappedoctetstr) != 2:
      raise ValueError("Quoted string is poorly formed")

    resultstr = \
        chr(int(wrappedoctetstr, 16)) + \
        string[lastpercentlocation+3:] + \
        resultstr
    string = string[:lastpercentlocation]

  resultstr = string + resultstr
  return resultstr




def urllib_unquote_plus(string):
  """
  <Purpose>
    Unquote the urlencoded query fragment of a URL.

  <Arguments>
    string:
           The string to unquote.

  <Exceptions>
    ValueError thrown if the last wrapped octet isn't a valid wrapped octet
    (i.e. if the string ends in "%" or "%x" rather than "%xx". Also throws
    ValueError if the nibbles aren't valid hex digits.

  <Side Effects>
    None.

  <Returns>
    The decoded string.
  """

  return urllib_unquote(string.replace("+", " "))




def urllib_quote_parameters(dictionary):
  """
  <Purpose>
    Encode a dictionary of (key, value) pairs into an HTTP query string or
    POST body (same form).

  <Arguments>
    dictionary:
           The dictionary to quote.

  <Exceptions>
    None.

  <Side Effects>
    None.

  <Returns>
    The quoted dictionary.
  """

  quoted_keyvals = []
  for key, val in dictionary.items():
    quoted_keyvals.append("%s=%s" % (urllib_quote(key), urllib_quote(val)))

  return "&".join(quoted_keyvals)




def urllib_unquote_parameters(string):
  """
  <Purpose>
    Decode a urlencoded query string or POST body.

  <Arguments>
    string:
           The string to decode.

  <Exceptions>
    ValueError if the string is poorly formed.

  <Side Effects>
    None.

  <Returns>
    A dictionary mapping keys to values.
  """

  keyvalpairs = string.split("&")
  res = {}

  for quotedkeyval in keyvalpairs:
    # Throw ValueError if there is more or less than one '='.
    quotedkey, quotedval = quotedkeyval.split("=")
    key = urllib_unquote(quotedkey)
    val = urllib_unquote(quotedval)
    res[key] = val

  return res




def server_test_content(httprequest_dictionary, http_query, http_post):
  # temp server that sends the clients posted data as the http content   
      
  # return the content to check if the httpretrieve gets the same content 
  return [httprequest_dictionary['posted_data'], None]
  
  
       
if callfunc == 'initialize':

  # data to post to server using the httpretrieve 
  http_post={"first": "1st", "second": "2nd"}
    
  # build temp server that acts normally and sends what ever the client posted data is
  try:    
    server_handle = registerhttpcallback('http://127.0.0.1:12345', server_test_content)
  except Exception, e:
    raise Exception('Server failed internally ' + str(e))  

  try:
    # use httpretrieve to retrieve the content form the server.(which is the posted data)  
    recv_msg = httpretrieve_get_string('http://127.0.0.1:12345', None, http_post)   

  except Exception, e:
    print 'Http retrieve failed on receiving content, Raised: ' + str(e)
  else:
    # check if the recieved post is similar to the http post sent                               
    if recv_msg != urllib_quote_parameters(http_post):
      print 'failed: the received posted data didnt match the actual posted data'
      print 'httpretrieve posted ' + urllib_quote_parameters(http_post)
      print 'server receieved ' + recv_msg 
  
  finally:
    #stop the server from waiting for more connections
    stop_registerhttpcallback(server_handle)
