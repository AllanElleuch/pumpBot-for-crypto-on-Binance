import logging
from logging.config import fileConfig
logging.config.fileConfig('logging_config.ini', defaults={'logfilename': 'logs/main.log'})



def getLogger(logerName):
  return logging.getLogger(logerName)


def getLoggerFilename(logerName,fileName):
  logging.config.fileConfig('logging_config.ini', defaults={'logfilename': 'logs/'+fileName})
  return logging.getLogger(logerName)
