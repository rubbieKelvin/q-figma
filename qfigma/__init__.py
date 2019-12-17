import base64
import requests

# FUNCTIONS
def requestfigmafile(token, fileid):
	resp = requests.get(f"https://api.figma.com/v1/files/{fileid}", headers={'X-Figma-Token': token})

	if resp.status_code == 200:
		return resp.json()
	else:
		return None

def jibberish(string):
	return base64.b16encode(bytes(string, "utf8")).decode("utf8")
