import logging
from logging.config import fileConfig
logging.config.fileConfig('logging_config.ini', defaults={'logfilename': 'mylog.log'})



def getLogger(logerName):
  return logging.getLogger(logerName)

