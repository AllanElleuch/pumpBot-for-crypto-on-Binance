import json
import logging
from logging.config import fileConfig
from BinanceRestAPI import BinanceRestAPI
import sys
from datetime import datetime
from Logger import getLogger
from strategie_simple import simple_strategy

logger = getLogger("MAIN")

logger.info('Starting %s', 'MoonBot')

binanceRestAPI =  BinanceRestAPI()

if __name__ == "__main__":
  asset = sys.stdin.readline()
  asset = str(asset).upper().replace('\n', '')
  simple_strategy(client=binanceRestAPI, symbolTargetCoin=asset,quantityInBTCToSpend=0.0002,allIn=False) #0.265

