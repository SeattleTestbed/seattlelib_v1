"""
<Purpose>
  Test the IP validation for geoip_client.repy
  Function Tested:
    _isvalidIP()

<Description>
  Related to ticket #1168, where the GeoIP server processes IP address
  that are in invalid format and returns results of some random IP. A
  check has been made in the geoip_client.repy library file to validate
  the IP address before passing the IP address to the server.
"""

import repyhelper
repyhelper.translate_and_import('geoip_client.repy')

geoip_init_client()

# Test an IP address with invalid length...
try:
  ret = geoip_record_by_addr('1122.233.69')
except ValueError, err:
  if str(err) != 'Not a valid IPv4 address.':
    raise
else:
  raise Exception, "[Failed]" + str(err)

# Test an IP address with decimal value not in range 0-255...
try:
  ret = geoip_record_by_addr('1122.233.69.123')
except ValueError, err:
  if str(err) != 'Not a valid IPv4 address.':
    raise
else:
  raise Exception, "[Failed]" + str(err)

# Test an IP address with alpha-numberic values...
try:
  ret = geoip_record_by_addr('112.b.23.34')
except ValueError, err:
  if str(err) != 'Not a valid IPv4 address.':
    raise
else:
  raise Exception, "[Failed]" + str(err)

# Test if a valid IP address is raising any error...
try:
  ret = geoip_record_by_addr('173.194.43.18')
except ValueError, err:
  raise Exception, "[FAILED]" + str(err)
