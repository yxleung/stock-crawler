import time
import datetime
import threading
from src.config import logger
from src.data_sources.sina_us_stock import main as sina_main
from src.data_sources.yahoo_us_stock import main as yahoo_main


def daemon(do=False):
    """定时器"""
    now = datetime.datetime.now()
    minute = int(now.strftime("%M"))
    hour = int(now.strftime('%H'))
    # 每天早上8点运行
    if (hour == 8 and minute == 0) or do:
        for _ in range(10):
            try:
                register()
                break
            except Exception as e:
                logger.exception(e)
                time.sleep(60 * 60)
    timer = threading.Timer(60, daemon)
    timer.start()


def register():
    sina_main()
    yahoo_main()
