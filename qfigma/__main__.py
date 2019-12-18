import os
import json
from . import requestfigmafile

token = input("Enter your token: ")
file_id = input("Enter file id: ")

response = requestfigmafile(token, file_id)

if type(response) is dict:
	filename = file_id+".json"

	print("request successful.")
	print("writing into", filename)
	
	with open(filename, "w") as file:
		json.dump(response, file, indent=2)

	print(f"figma file {file_id} saved into {filename}")
else:
	print("failed to fetch figma file.")
