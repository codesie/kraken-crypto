# https://github.com/veox/python3-krakenex/blob/742aed50e7568a3561b10c439458359b52332e61/krakenex/api.py
import requests
import time
import json

import urllib.parse
import hashlib
import hmac
import base64


kraken_url = "https://api.kraken.com"
ticker_path = "/0/public/Ticker"


def main():
    config = getConfig()
    # 1 - Get current ask price
    query_params = "?pair=" + ",".join(config["pairs"])
    ticker_result = publicCall(kraken_url + ticker_path, query_params)
    print(json.dumps(ticker_result, indent=2))

    for pair in config["pairs"]:
        bid_price = float(ticker_result["result"][pair]["b"][0])
        print(pair + ": " + str(bid_price))

        # 2 - Create order
        data = {
            "pair": pair,
            "type": "buy",
            "ordertype": "limit",
            "price": bid_price,
            "volume": (config["investEurPerTrade"] / bid_price)
        }
        add_order_path = "/0/private/AddOrder"
        # print(data)
        privateCall(add_order_path, data)


def privateCall(private_path, data):
    config = getConfig()

    data["nonce"] = generateNonce()

    print(data)

    headers = {
        'API-Key': config["api_key"],
        'API-Sign': generateApiSign(private_path, data, config["secret"]),
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    print(headers)

    response = requests.request(
        "POST", kraken_url + private_path, headers=headers, data=data)

    print(json.dumps(response.json(), indent=2))


def publicCall(url, query_params):

    payload = {}
    headers = {}

    url = url + query_params
    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def generateNonce():
    return int(1000*time.time())


def generateApiSign(private_path, data, secret):
    postdata = urllib.parse.urlencode(data)

    # Unicode-objects must be encoded before hashing
    encoded = (str(data['nonce']) + postdata).encode()
    message = private_path.encode() + hashlib.sha256(encoded).digest()

    signature = hmac.new(base64.b64decode(secret),
                         message, hashlib.sha512)

    sigdigest = base64.b64encode(signature.digest())

    return sigdigest.decode()


def getConfig():
    with open("../config.json") as file:
        config = json.load(file)
    return config


if __name__ == "__main__":
    main()
