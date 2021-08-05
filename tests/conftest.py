import logging
from rich.logging import RichHandler

logging.basicConfig(level=logging.DEBUG, handlers=[RichHandler()])
