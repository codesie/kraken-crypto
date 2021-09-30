import os
import json
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
