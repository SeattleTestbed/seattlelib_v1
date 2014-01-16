"""
<Purpose>
  Ensures that private IP addresses trigger proper exceptions.
  See #1280.

"""

import repyhelper
repyhelper.translate_and_import("geoip_client.repy")

geoip_init_client()

private_ips = ["10.0.0.0", "172.16.0.0", "192.168.0.0"]
for ip in private_ips:
  try:
    geoip_record_by_addr(ip)
  except Exception, e:
      if "Not a public IP address" not in str(e):
        raise
  else:
    raise Exception("Private IP address silently failed!")
