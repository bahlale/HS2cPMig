import sys
import pycpanel
import json
import os
import ConfigParser

def main():
  cpanel_config = False

  # Check if ./.cpanel.cnf exists
  if os.path.isfile("./.cpanel.cnf"): 
    cpanel_config = "./.cpanel.cnf"
  if not cpanel_config:
    print "Could not get the config file please save the cPanel login details in ./.cpanel.cnf"
    sys.exit(0)
  else:
    # Read config file
    config = ConfigParser.ConfigParser()
    config.read(cpanel_config)

    # Try to get the cPanel Server IP
    try: cpanel_server = config.get('cpanel', 'host')
    except Exception, e: 
      print ("Could not get any cPanel Server information from %s." % (cpanel_config))
      sys.exit(0)

    # Try to get the cPanel user
    try: cpanel_user = config.get('cpanel', 'user')
    except Exception, e: 
      print ("Could not get any cPanel user information from %s." % (cpanel_config))
      sys.exit(0)
        
    # Try to get the cPanel user password
    try: cpanel_password = config.get('cpanel', 'password')
    except Exception, e:
      print ("Could not get any cPanel password information from %s." % (cpanel_config))
      sys.exit(0)   
  print (cpanel_server,cpanel_user,cpanel_password)
  server = pycpanel.conn(hostname=cpanel_server, username=cpanel_user, 
  	                   hash=None, password=cpanel_password, ssl=True, verify=False, check_conn=False)
  params = {
    'dir'       : str(sys.argv[1]),
    'newdomain' : str(sys.argv[2]),
    'subdomain' : str(sys.argv[3])  
  }

  res = server.cpanel_api('AddonDomain', 'addaddondomain', str(sys.argv[4]), params=params)
  data = json.loads(json.dumps(res[0]))
  if data['result'] == 1:
    print ("Addon domain %s created successfully" % str(sys.argv[2]))
  else:
	  print ("Addon domain %s is not created due to %s" % (str(sys.argv[2]), data['reason']))


if __name__ == "__main__":
  main()  