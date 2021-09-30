import base64
import hmac
import hashlib
import urllib.parse
import requests
import time
import json
import argparse
import os
import logging
import logging.handlers as handlers


kraken_url = "https://api.kraken.com"
ticker_path = "/0/public/Ticker"


def main(args, logger):
    """
    Main function of the script. Queries the current bid prices of the provided currencies and
    sends the order to the kraken api, if mode prod is provided.

    args (Namespace): contains the provided arguments. ex: Namespace(mode='debug')
    logger (logging): logging handler for writing to the log file
    """
    config = getConfig()
    # 1 - Get current ask price
    query_params = "?pair=" + ",".join(config["pairs"])
    ticker_result = publicCall(ticker_path, query_params)
    logger.debug(json.dumps(ticker_result, indent=2))

    for pair in config["pairs"]:
        # last ask price
        # price = float(ticker_result["result"][pair]["b"][0])
        # 24 h lowest price
        price = float(ticker_result["result"][pair]["l"][0])

        # 2 - Create order
        data = {
            "pair": pair,
            "type": "buy",
            "ordertype": "limit",
            "price": price,
            "volume": (config["investEurPerTrade"] / price)
        }
        add_order_path = "/0/private/AddOrder"
        # print(data)
        if args.mode == "prod":
            logger.info("--- Order placed on kraken!")
            logger.info("Investing: " +
                        str(config["investEurPerTrade"]) + " euros in " + pair)
            logger.info(json.dumps(data, indent=2))
            privateCall(add_order_path, data, logger)
        else:
            logger.info(
                "--- No order placed on kraken! Shows the order which would have been executed in prod mode.")
            logger.info("Investing: " +
                        str(config["investEurPerTrade"]) + " euros in " + pair)
            logger.info(json.dumps(data, indent=2))


def privateCall(private_path, data, logger):
    """
    Executes private api calls. Private calls need authentication, which is implemented in
    this function.

    Parameters:
    private_path (str): target of the private api. ex: "/0/private/AddOrder"
    data (dict): necessary data for the request. ex: {'pair': 'XXBTZEUR', 'type': 'buy', 'ordertype': 'limit', 'price': 47633.1, 'volume': 0.001049690236411235}
    logger (logging): logging handler for writing to the log file
    """
    config = getConfig()

    data["nonce"] = generateNonce()

    headers = {
        'API-Key': config["api_key"],
        'API-Sign': generateApiSign(private_path, data, config["secret"]),
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    logger.debug(headers)

    response = requests.request(
        "POST", kraken_url + private_path, headers=headers, data=data)

    logger.info(json.dumps(response.json(), indent=2))


def publicCall(public_path, query_params):
    """
    Executes public api calls. No need for authentication.

    Parameters:
    public_path (str): target of the private api. ex: "/0/public/Ticker"
    query_params (str): query parameters for specifying, what we want. ex: "?pair=XXBTZEUR"

    Returns:
    json:response from the api
    """
    payload = {}
    headers = {}

    url = kraken_url + public_path + query_params
    response = requests.request(
        "GET", url, headers=headers, data=payload)

    return response.json()


def generateNonce():
    """
    Generates the nonce.

    Sources:
    https://www.kraken.com/features/api#general-usage
    https://github.com/veox/python3-krakenex/blob/742aed50e7568a3561b10c439458359b52332e61/krakenex/api.py
    """
    return int(1000*time.time())


def generateApiSign(private_path, data, secret):
    """
    Generates the api sign key.

    Sources:
    https://www.kraken.com/features/api#general-usage
    https://github.com/veox/python3-krakenex/blob/742aed50e7568a3561b10c439458359b52332e61/krakenex/api.py
    """
    postdata = urllib.parse.urlencode(data)

    # Unicode-objects must be encoded before hashing
    encoded = (str(data['nonce']) + postdata).encode()
    message = private_path.encode() + hashlib.sha256(encoded).digest()

    signature = hmac.new(base64.b64decode(secret),
                         message, hashlib.sha512)

    sigdigest = base64.b64encode(signature.digest())

    return sigdigest.decode()


def getConfig():
    """
    Get the content of the config.json file, which includes the amount of euros to spend per trade, which
    currencies to trade and more.

    Returns:
    json:Content of the file
    """
    script_dir = os.path.dirname(__file__)
    config_file = os.path.join(script_dir, "..", "config.json")
    print(config_file)
    with open(config_file) as file:
        config = json.load(file)
    return config


def initializeLogger():
    """
    Here a logger is initialized. It displays outputs in the console and logs them as well to
    a log file. Thereby we have a persistent history of our file execution.

    logging:the logger object
    """
    try:
        logger = logging.getLogger("kraken_crypto")
        logger.setLevel(logging.INFO)

        init_formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

        script_dir = os.path.dirname(__file__)
        log_file = os.path.join(script_dir, "..", "logs", "kraken_crypto.log")
        init_handler = logging.FileHandler(log_file)
        init_handler.setFormatter(init_formatter)

        init_stream = logging.StreamHandler()
        init_stream.setLevel(logging.INFO)
        init_stream.setFormatter(init_formatter)

        logger.addHandler(init_handler)
        logger.addHandler(init_stream)
        return logger
    except Exception as e:
        print("logger.initial_setup\n"
              "- " + str(e))


if __name__ == "__main__":
    """
    Main entry of the script. First, the provided arguments are parsed and then the main purpose of the script is 
    executed.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m", "--mode", help="run the script in demo mode, without executing the order, or in production mode, which places an order.", default="demo")
    args = parser.parse_args()
    logger = initializeLogger()
    main(args, logger)
