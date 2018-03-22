from __future__ import print_function
import httplib2
import os
import sys

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.file'\
		+' https://www.googleapis.com/auth/drive.metadata.readonly'\
		+' https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
		Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,
								   'drive-python-quickstart.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

def download():
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('drive', 'v3', http=http)

	name = "Songs";
	files = service.files().list(q="name = '"+name+"'").execute().get('files',[])
	if (len(files) == 0):
		raise FileNotFoundError("Could not find file named "+name+" in your Drive.");
	file_id = files[0]['id']
	data = service.files().export(fileId=file_id,
												 mimeType='text/tab-separated-values').execute();
	if data:
		fn = 'data.txt'
		with open(fn, 'wb') as fh:
			fh.write(data)
	else:
		raise FileNotFoundError("Could not download file.")

def main():
	try:
		download()
	except FileNotFoundError as err:
		sys.stderr.write(err.args[0]+"\n")
		sys.exit(1)	

if __name__ == '__main__':
	main()