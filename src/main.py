import threading
from src.config import logger
from src.us_stock import daemon

if __name__ == '__main__':
    threading.Thread(target=daemon).start()
    logger.info('server started.')
