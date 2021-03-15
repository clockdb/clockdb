from φ.models import *
import requests
import json

params = {
  'access_key': 'ecae621d4718099f0d660a237c429450',
  'symbols': 'AAPL',
}

api_result = requests.get('https://api.marketstack.com/v1/tickers/aapl/eod', params)

api_response = api_result.json()

api_result_name = api_result.json()['data']['name']
api_result_symbol = api_result.json()['data']['symbol']
api_result_date = api_result.json()['data']['eod'][0]['date']
api_result_stockprice = api_result.json()['data']['eod'][0]['close']


print(api_result_name)
print(api_result_symbol)
print(api_result_date)
print(api_result_stockprice)