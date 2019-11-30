import threading
from src.config import logger
from src.us_stock import daemon

if __name__ == '__main__':
    threading.Thread(target=daemon, args=(True,)).start()
    logger.info('server started.')
