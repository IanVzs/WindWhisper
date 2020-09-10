import logging
import logging.config

logging.config.fileConfig('logging.ini')

# create wea logger
weatherLog = logging.getLogger('weatherLog')
debugLog = logging.getLogger('debugLog')