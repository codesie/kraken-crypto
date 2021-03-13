# kraken-crypto

Interacting with Kraken Crypto Exchange API

## standing-order

Execute an automated buy of cryptos. My use case: I want to invest money on a regualr basis in cryptos. As I am not a trader, I dont wanna loose to much time doing this. This script can be scheduled with crontab and be executed once a month. It generates an order for your pairs in the config.json file on the current bid price. It needs to be verified on the gui or with further API calls, if the order was executed successfully.
We see the outputs of the script in the console, but this outputs are logged as well in logs/kraken_crypto.log.

### Setup

A config.json file is required in the folder kraken-crypto, which contains API-Key, API-Secret, Pairs and an amount to invest per crypto. Have a look at config-example.json.

### Execution

The script can be executed with a mode argument. This gives us the possibility to run the script in debug mode, which shows us, the order which would have been placed on the kraken exchange. If no argument is provided the debug mode is default. So if the script is executed as shown below:

```
python3 standing-order/trade.py
```

You see what orders would have been placed, but they are NOT sent to kraken.

If we want the script to send the order to kraken, we need to provide the argument "prod".

```
python3 standing-order/trade.py -m prod
```
