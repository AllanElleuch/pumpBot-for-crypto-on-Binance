from binance.client import Client
import json 



with open('config-binance.json') as json_data:
  api_config = json.load(json_data)
  json_data.close()


client = Client(api_config['api_key'], api_config['api_secret'])
