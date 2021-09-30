import base64
import hmac
import hashlib
import urllib.parse
import requests
import time
import json
import csv
import os
import logging
import logging.handlers as handlers


kraken_url = "https://api.kraken.com"
ticker_path = "/0/public/Ticker"


def main(logger):
    """
    Main function of the script. Gets all trades and consolidates the data.

    logger (logging): logging handler for writing to the log file
    """

    # 2 - Create order
    result_offset = 0
    all_pairs = {}
    # sum = 0
    new_results = True

    data_file = open("logs/data_file.csv", "w")
    json_file = open("logs/trades.json", "w")
    json_data = {}
    csv_writer = csv.writer(data_file)
    set_header = True

    while new_results:
        logger.info("-- Get trade history with offset: " + str(result_offset))
        # query the trading history from the api
        result = getTradeHistory(result_offset, logger)

        json_data.update(result["result"]["trades"])

        # loop through the result
        for trade_id in result["result"]["trades"]:
            trade = result["result"]["trades"][trade_id]
            if trade["pair"] not in all_pairs:
                all_pairs[trade["pair"]] = []
            all_pairs[trade["pair"]].append(float(trade["vol"]))
            logger.info(time.ctime(
                trade["time"]) + " - Pair: " + trade["pair"] + " - Vol: " + trade["vol"] + " Type: " + trade["type"])
            if set_header:
                csv_writer.writerow(trade)
                set_header = False

            csv_writer.writerow(trade.values())

        if result_offset < result["result"]["count"]:
            result_offset += 50
        else:
            new_results = False

        # logger.info(json.dumps(result["result"], indent=2))
    # logger.info("Polkadot Total: " + str(sum))
    logger.info("All pairs: " + str(all_pairs))
    json.dump(json_data, json_file)


def getTradeHistory(result_offset, logger):
    """
    Executes private api calls. Private calls need authentication, which is implemented in
    this function.

    Parameters:
    private_path (str): target of the private api. ex: "/0/private/AddOrder"
    data (dict): necessary data for the request. ex: {'pair': 'XXBTZEUR', 'type': 'buy', 'ordertype': 'limit', 'price': 47633.1, 'volume': 0.001049690236411235}
    logger (logging): logging handler for writing to the log file
    """
    config = getConfig()

    data = {}

    data["nonce"] = generateNonce()
    data["ofs"] = result_offset

    headers = {
        'API-Key': config["api_key"],
        'API-Sign': generateApiSign("/0/private/TradesHistory", data, config["secret"]),
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    # logger.debug(headers)

    response = requests.request(
        "POST", kraken_url + "/0/private/TradesHistory", headers=headers, data=data)

    # logger.info(json.dumps(response.json(), indent=2))
    return response.json()


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
    config_file = os.path.join(script_dir, "config.json")
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
        logger = logging.getLogger("get_trade_history")
        logger.setLevel(logging.INFO)

        init_formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

        script_dir = os.path.dirname(__file__)
        log_file = os.path.join(script_dir, "logs", "getTrades.log")
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
    logger = initializeLogger()
    main(logger)
