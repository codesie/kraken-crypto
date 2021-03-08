# kraken-crypto

Interacting with Kraken Crypto Exchange API

## Standing-order

Execute an automated buy of cryptos. My use case: I want to invest money on a regualr basis in cryptos. As I am not a trader, I dont wanna loose to much time doing this. This script can be scheduled with crontab and be executed once a month. It generates an order for your pairs in the config.json file on the current bid price. It needs to be verified on the gui or with further API calls, if the order was executed successfully.
