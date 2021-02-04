import json
import logging
from logging.config import fileConfig
from BinanceRestAPI import BinanceRestAPI
import sys
from datetime import datetime
from Logger import getLogger
logger = getLogger("MAIN")

logger.info('Starting %s', 'MoonBot')


if __name__ == "__main__":
  asset = sys.stdin.readline()
  asset = str(asset).upper().replace('\n', '')
