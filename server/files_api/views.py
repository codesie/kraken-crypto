import os
import json
import time
from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(["GET"])
def TradeList(request):
    settings_dir = os.path.dirname(__file__)
    API_DATA_FOLDER = os.path.join(settings_dir, "data")
    TRADES_FILE = os.path.join(API_DATA_FOLDER, "trades.json")
    with open(TRADES_FILE, "r") as trades:
        data = trades.read()

    return JsonResponse(json.loads(data))


def TradesOverview(request):
    settings_dir = os.path.dirname(__file__)
    API_DATA_FOLDER = os.path.join(settings_dir, "data")
    TRADES_FILE = os.path.join(API_DATA_FOLDER, "trades.json")
    with open(TRADES_FILE, "r") as trades:
        data = trades.read()

    result = consolidate(json.loads(data))

    return JsonResponse(result, safe=False)


def consolidate(jsonData):
    temporary = {}
    for id in jsonData:
        pair = jsonData[id]["pair"]
        volume = float(jsonData[id]["vol"])
        trading_date = jsonData[id]["time"]
        print(trading_date)

        if time.localtime(trading_date).tm_year >= 2021:
            if pair not in temporary:
                temporary[pair] = {"volumeBuy": [], "volumeSell": []}

            if jsonData[id]["type"] == "buy":
                if pair in temporary:
                    temporary[pair]["volumeBuy"].append(volume)
            else:
                if pair in temporary:
                    temporary[pair]["volumeSell"].append(volume)
            # print(jsonData[id])

    result = []
    for pair in temporary:
        volumeBuy = sum(temporary[pair]["volumeBuy"])
        volumeSell = sum(temporary[pair]["volumeSell"])
        result.append({"pair": pair, "volumeBuy": (
            volumeBuy - volumeSell), "volumeSell": volumeSell})
    return result
