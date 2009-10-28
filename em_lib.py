"""

<Program Name>
     em_lib.repy (expirament manager library)

<Authors>
    Eric Kimbrel (kimbrl@cs.washington.edu)
    Justin Sammuel (jsamuel@cs.gmail.edu)

<Purpose>

  Provide a general library with simple to use abstractions for the acquistion and operation of Seattle testbed vessels.

  
 General philosophy  ( Probably delete this when the file is finished )

   1. within this library there should be only one representation of a resource
      we may have to create a new abstraction on top of other represenations to 
      handle this.  The idea is to make it easy to understand for a user.
 
   2. fuctions should always act on a list of resources rather than a single resource

   3. there should be only one way to identify yourself, i.e. one abstraction type for identity.

"""

# the max time one can renew a resource for
MAX_RENEW_TIME = ???


####      ID MANAGEMENT FUNCTIONS          ####


def em_load_keys(user_name,path='./'):
  """
  <Purpose>
    create an identity from previously stored public and private keys

  <Arguments>
    user_name  the name of the public and private key files
      for example user_name='joe' implies there are two files
      joe.publickey
      joe.privatekey
   
    path  -  The path to the key files

  <Exceptions>
    TODO, FILL IN EXCEPTION TYPES

  <Returns>
    an identity object to be used with other calls in this module
  """
  pass


####                       RESOURCE MANAGEMENT                  ####
####  Search for, contact, acquire, release, or renew resouces  ####


def em_browse(identity):
  """
  <Purpose>
    Browse for resource available to the specified identity

  <Arguments>
    identity - the identity object returned by em_load_keys
  
  <Exceptions>

  <Returns>
    A list of resources  

  """
  pass



def em_contact(identity,host,port):
  """
  <Purpose>
    Attempt to contact a node manager and get a resource handle
    Resource handle is only given if the identity has been granted
    the resource on this node.

  <Arguments>
    identity - the identity object returend by em_loadkeys
    host - the host name or ip address of a node manager
    port - the control port of the nodemanger

  <Exceptions>
    rasies an exception if no resources have been granted to the identity on this node, or if a communication error occurs

  <Returns>
    a resource object  

  """
  pass


def em_acquire_resources(identity,type,number)
  """
  <Purpose>
    Acquire resources of a certain type

  <Arguments>
    identity - the identity object returend by em_loadkeys
    type - the type of resource to be aqcuired, 'wan' 'lan' 'random' or 'nat'

  <Exceptions>
    no nodes are acquired

  <Returns>
    a list of resources that have been succesfully acquired
  """
  pass




# what if i release a resource that has been split, but only realeas part of it
def em_release_recources(identity,resource_list):
  """
  <Purpose>
    Release a list of resources

  <Arguments>
    identity - the identity object returend by em_loadkeys
    resource_list  -  a list of resources

  <Exceptions>
    
  <Returns>
    a tuple of the form (True,None) of (False,unreleased_resource_list)

  """
  pass


# re-new resources
   # what if i re-new a vessl that has been splitk but only renew part?
def em_renew_resources(identity,resource_list,time=MAX_RENEW_TIME):
  """
  <Purpose>
    renew a list of resources before they expire

  <Arguments>
    identity - the identity object returend by em_loadkeys
    resource_list - the list of rescoures to renew
    time  - the ammount of time to renew for

  <Exceptions>

  <Returns>
    A tupe of the form (True,None) of (False,un-renewed_resource_list)
  """
  pass


####         VESSEL CONTROL      ####


# wait_for_status(vessel_list,target_status,callbackfunction,checktime=10minutes)
def em_wait_for_status(identity,resource_list,status,callback,checktime=600)
  """
  <Purpose>
    Trigger a call back fucntion with arguments
  
    (identity,resource,status) whenever a nodes status is equl to the status specified.  Each nodes status is checked every checktime seconds

  <Arguments>
    identity - the identity object returned by em_loadkeys
    resource_list  - a list of resources to check
    status    -  the target statuse
    callback  - the callback function 
    checktime - how often to check status

  <Exceptions>

  <Returns>
    a status_handle
  """
  pass



def em_stopcheck(status_handle):
  """
  <Purpose>
    Stop the callback function from a previous wait_for_status call from being
    executed
    
  <Arguments>
    status_handle, a handle returned by wait_for_status

  <Exceptions>

  <Returns>
    True or False
  """
  pass




def em_list(identity,resource_list)
  """
  <Purpose>
    List information about a resource
  <Arguments>

  <Exceptions>

  <Returns>

  """
  pass



def em_show_logs(identity,resource_list)
 """
  <Purpose>
    get the logs from a list of resources
  <Arguments>

  <Exceptions>

  <Returns>

  """
  pass



def em_clear_log(identity,resource_list):
"""
  <Purpose>
    Clear the logs (without stoping the vessels)
  <Arguments>

  <Exceptions>

  <Returns>

"""
  pass



def em_upload(identity,resource_list,file)
  """
  <Purpose>

  <Arguments>

  <Exceptions>

  <Returns>

  """
  pass


def em_download(identity,resource_list,file)
 """
  <Purpose>
    download a file
  <Arguments>

  <Exceptions>

  <Returns>

"""
  pass


def em_delete(identity,resource_list,file)
 """
  <Purpose>
    Delete a file from the vessles
  <Arguments>

  <Exceptions>

  <Returns>

"""
  pass


def em_reset(identity,resource_list)
 """
  <Purpose>
    stop the vessles and clear all state
  <Arguments>

  <Exceptions>

  <Returns>

"""
  pass



def em_start(identity,resource_list,file,arg_string)
 """
  <Purpose>
    start a file (previously uploaded) on the vessels

  <Arguments>

  <Exceptions>

  <Returns>

"""
  pass


def em_stop(identity,resource_list)
"""
  <Purpose>
    Stop a running vessle
  <Arguments>

  <Exceptions>

  <Returns>

"""
  pass



def em_split(identity,resource_list)
"""
  <Purpose>
    Split each vessle into two new vessels
  <Arguments>

  <Exceptions>

  <Returns>

"""
  pass


def em_join(identity,resource_list):
"""
  <Purpose>
    Join a set of vessels on the same node into one vessel
  <Arguments>

  <Exceptions>

  <Returns>

"""
  pass



