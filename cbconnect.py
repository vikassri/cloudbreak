import requests
from six.moves.urllib import parse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json, os

class CbExceptions(Exception):
	pass

class cbconnect(object):
	__token = None
	__user = None
	__pass = None
	__host = None
	__header = None
	
	def __init__(self,*args, **kwargs):
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		''' we either get the details from the os environment or from keyword arguments '''
		if len(kwargs) == 0 :
			if os.getenv('cbhost'):
				self.__host = os.getenv('cbhost')
			if os.getenv('cbuser'):
				self.__user = os.getenv('cbuser')
			if os.getenv('cbpass'):
				self.__pass = os.getenv('cbpass')
			else :
				raise CbExceptions('Hostname/user/pass not set, Aborting !')

		if len(kwargs) == 3:
			if kwargs.get('cbhost'):
				self.__host = kwargs.get('cbhost')
			if kwargs.get('cbuser'):
				self.__user = kwargs.get('cbuser')
			if kwargs.get('cbpass'):
				self.__pass = kwargs.get('cbpass')
			else :
				raise CbExceptions('host/user/pass is missing, Aborting !')

		url = 'https://' + self.__host + '/identity/oauth/authorize'
		try :
			resp = requests.post( url=url, params={ 'response_type': 'token',
        	'client_id': 'cloudbreak_shell',
        	'scope.0': 'openid',
        	'source': 'login',
        	'redirect_uri': 'http://cloudbreak.shell' },
    		headers={'accept': 'application/x-www-form-urlencoded'},
    		verify=False,
    		allow_redirects=False,
    		data=[('credentials', '{"username":"' + self.__user  + '",''"password":"' + self.__pass + '"}'),])
			resp.raise_for_status()
			token = parse.parse_qs(resp.headers["Location"])['access_token'][0]
			self.__token = str(token)
			self.__header = {'Authorization': 'Bearer {}'.format(token),'Content-Type': 'application/json'}
		except:
			raise CbExceptions("Unable to connect to get Authentication Token, status_code : {}".format(resp.status_code)) 

#####  WorkSpace API's #############
	def ListWorkSpaces(self, **kwargs):
		""" Find the workspaces """
		api = "https://" + self.__host + "/cb/api/v3/workspaces"
		try :
			req = requests.get(api,headers= self.__header, verify=False)
		except:
			raise CbExceptions('could not communicate with API')

		if req.status_code == 200:
			json_file = json.loads(req.text)
			if kwargs.get('id'):
				for workspace in json_file:
					userids = []
					for userid in workspace['users']:
						userids.append(userid['userId'])
					if workspace['id'] == kwargs.get('id'):
						print("Id = {}, Name = {} , Status = {}, Userlist = {}" .format(workspace['id'], workspace['name'], workspace['status'], userids))
			if kwargs.get('name'):
				for workspace in json_file:
					userids = []
					for userid in workspace['users']:
						userids.append(userid['userId'])
					if workspace['name'] == kwargs.get('name'):
						print("Id = {}, Name = {} , Status = {}, Userlist = {}" .format(workspace['id'], workspace['name'], workspace['status'], userids))              
			if len(kwargs) == 0:
				for workspace in json_file:
					userids = []
					for userid in workspace['users']:
						userids.append(userid['userId'])
					print("Id = {} \t Name = {} \t Status = {} \t Userlist = {}" .format(workspace['id'], workspace['name'], workspace['status'], userids))
		else :
			raise CbExceptions('Unable to connect to API: status_code :', req.status_code)

		def ListStacks(self, **kwargs):
		api = "https://" + self.__host + "/cb/api/v1/stacks/user"
		try :
			req = requests.get(api,headers= self.__header, verify=False)
		except:
			raise CbExceptions('Could not communicate with Stacks API')

		if req.status_code == 200:
			json_file = json.loads(req.text)
			#print(json.dumps(json_file, indent=4, sort_keys=True))
			for account in json_file:
				if kwargs.get('clustername') == account['name']:
					print("HDPVersion: {}, ClusterName: {}, AmbariURL: {}, AvailabilityZone: {}".format(account['hdpVersion'],account['name'],account['cluster']['ambariServerUrl'],account['availabilityZone']))
				if kwargs.get('Az') == account['availabilityZone']:
					print("HDPVersion: {}, ClusterName: {}, AmbariURL: {}, AvailabilityZone: {}".format(account['hdpVersion'],account['name'],account['cluster']['ambariServerUrl'],account['availabilityZone']))
				else :
					print("HDPVersion: {}, ClusterName: {}, AmbariURL: {}, AvailabilityZone: {}".format(account['hdpVersion'],account['name'],account['cluster']['ambariServerUrl'],account['availabilityZone']))
		else :
			raise CbExceptions('could not communicate with Stacks API')


	def ListStackWithWid(self, **kwargs):
		try :
			if kwargs.get('wid'):
				api = "https://" + self.__host + "/cb/api/v3/"+ str(kwargs.get('wid')) +"/stacks/" 
				req = requests.get(api,headers= self.__header, verify=False)
			else :
				raise CbExceptions('workspaceid parameter is missing, please provide (wid=$number) in function')
		except:
			raise CbExceptions('Could not communicate with Stacks API')

		if req.status_code == 200:
			json_file = json.loads(req.text)
			for account in json_file:
				print("StackId: {}, StackName: {}, AmbariIP: {}, HDPVersion: {}, NodeCount: {}".format(account['id'],account['name'],account['cluster']['ambariServerIp'], account['cluster']['blueprint']['stackVersion'],account['nodeCount']))
		else :
			raise CbExceptions('could not communicate with Stacks API')

	
	def __str__(self):
		''' orverride of string funtion be carefull '''
		return f"{self.__class__.__name__}(hostname = {self.__host}, username = {self.__user} , password = '*****' )"

	def __format__(self):
		''' orverride of format funtion be carefull '''
		return f"{self.__class__.__name__}(hostname = {self.__host}, username = {self.__user} , password = '*****' )"

	def __repr__(self):
		''' orverride of repr funtion be carefull '''
		return f"{self.__class__.__name__}(hostname = {self.__host}, username = {self.__user} , password = '*****' )"

	def __unicode__(self):
		''' orverride of unicode funtion be carefull '''
		return f"{self.__class__.__name__}(hostname = {self.__host}, username = {self.__user} , password = '*****' )"






	

"""
export TOKEN=$(curl -k -iX POST -H "accept: application/x-www-form-urlencoded" -d 'credentials={"username":"test@gmail.com","password":"Password123"}'  "https://35.200.229.52/identity/oauth/authorize?response_type=token&client_id=cloudbreak_shell&scope.0=openid&source=login&redirect_uri=http://cloudbreak.shell" | grep Location | cut -d'=' -f 3 | cut -d'&' -f 1)
"""





