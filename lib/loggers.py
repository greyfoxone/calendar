import logging
import sys

level = logging.DEBUG
if "-debug" in sys.argv:
    print("DEBUG MODE")
    level = logging.DEBUG
    sys.argv.remove("-debug")

logger = logging.getLogger(__name__)
logger.setLevel(level)

c_handler = logging.StreamHandler()
c_handler.setLevel(level)
c_format = logging.Formatter("%(message)s")
c_handler.setFormatter(c_format)

f_handler = logging.FileHandler("error.log")
f_handler.setLevel(logging.ERROR)
f_format = logging.Formatter(
    "%(asctime)s %(levelname)s %(filename)s,%(funcName)s(%(lineno)d):%(message)s"
)
f_handler.setFormatter(f_format)
# remove previous handlers
logger.handlers.clear()
logger.addHandler(f_handler)
logger.addHandler(c_handler)