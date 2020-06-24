import logging
from rspv import rspv
from rspv.settings import *

_logger = logging.getLogger("console" if DEBUG else "")

if __name__ == '__main__':
    _logger.info("Starting Service")
    rspv.run()
