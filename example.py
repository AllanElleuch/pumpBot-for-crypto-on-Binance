import json
import logging
from logging.config import fileConfig
from BinanceRestAPI import BinanceRestAPI
import sys
from datetime import datetime
from Logger import getLogger
logger = getLogger("root")


logger.info('Starting %s at %s', 'MoonBot', datetime.now())

with open('config-binance.json') as json_data:
  api_config = json.load(json_data)
  json_data.close()


binanceRestAPI =  BinanceRestAPI()
logger.info('asset in account: %s', binanceRestAPI.getBalance("XVG"))

