import logging
import sys

logger = logging.getLogger()
default_handler = logging.StreamHandler(sys.stdout)
default_handler.setFormatter(logging.Formatter(
    '[%(asctime)s %(name)s] %(levelname)s: %(message)s'
))
logger.addHandler(default_handler)
