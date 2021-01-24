import logging
import logging.config

logging.config.fileConfig('logging.ini')

# create wea logger
backtaskLog = logging.getLogger('backtaskLog')
debugLog = logging.getLogger('debugLog')
scheLog = logging.getLogger('scheLog')
svrLog = logging.getLogger('svrLog')
