import json
import logging
from logging.config import fileConfig
from BinanceRestAPI import BinanceRestAPI


fileConfig('logging_config.ini')
logger = logging.getLogger()
logger.info('Starting %s', 'MoonBot')


with open('config-binance.json') as json_data:
  api_config = json.load(json_data)
  json_data.close()


binanceRestAPI =  BinanceRestAPI()

logger.info('asset in account: %s', binanceRestAPI.getBalance("XVG"))

