import logging
from logging.config import fileConfig



def getLogger(logerName):
  logging.config.fileConfig('logging_config.ini', defaults={'logfilename': 'mylog.log'})
  return logging.getLogger(logerName)

