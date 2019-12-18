import base64
import requests

# FUNCTIONS
def requestfigmafile(token, fileid):
	try: resp = requests.get(f"https://api.figma.com/v1/files/{fileid}", headers={'X-Figma-Token': token})
	except requests.exceptions.ConnectionError as e: return None
	
	if resp.status_code == 200: return resp.json()
	else: return None

def jibberish(string):
	# creates a random nonsense from $string
	# this is mostly used for uniqe identification in nodes
	return base64.b16encode(bytes(string, "utf8")).decode("utf8")
