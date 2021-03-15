from φ.models import *
import requests
import json

params = {
  'access_key': 'ecae621d4718099f0d660a237c429450',
}

api_result = requests.get('https://api.marketstack.com/v1/tickers/aapl/eod/2017-09-26', params)

api_response = api_result.json()

print(api_response)

api_result = api_result.json()['close']

print(api_result)
