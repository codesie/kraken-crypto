import requests
import json


public_url = "https://api.kraken.com/0/public/"
target = "Assets"
query_params = "?asset=ADA,DOT,ETH,XBT"


payload = {}
headers = {
}

url = public_url + target + query_params
response = requests.request("GET", url, headers=headers, data=payload)

print(json.dumps(response.json(), indent=2))
