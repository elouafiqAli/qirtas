import urllib, urlparse, subprocess

# Parameters of your app and the id of the profile you want to mess with.
FACEBOOK_APP_ID     = '891159394304371'
FACEBOOK_APP_SECRET = '70663d8d6725dfbb7a6cdd8989ee217e'


oauth_access_token = ''

def get_token():
		# Trying to get an access token. Very awkward.
	oauth_args = dict(client_id     = FACEBOOK_APP_ID,
	                  client_secret = FACEBOOK_APP_SECRET,
	                  grant_type    = 'client_credentials')
	oauth_curl_cmd = ['curl',
	                  'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)]
	oauth_response = subprocess.Popen(oauth_curl_cmd,
	                                  stdout = subprocess.PIPE,
	                                  stderr = subprocess.PIPE).communicate()[0]

	try:
	    oauth_access_token = urlparse.parse_qs(str(oauth_response))['access_token'][0]
	except KeyError:
	    print('Unable to grab an access token!')
	    exit()
	return oauth_access_token

