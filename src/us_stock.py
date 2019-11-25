import os
import json
import math
import time
import random
import string
import datetime
import requests
import threading
from tqdm import tqdm
from src.config import logger


def get_stock_num(url):
    """
    获取市场股票个数
    """
    random_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    resp = requests.get(url.format(random_str, 1))
    if resp.status_code != 200:
        raise RuntimeError(f'response status code:{resp.status_code}')
    text = resp.text.split('\n')[1]
    start = text.find('(') + 1
    end = -2
    json_obj = json.loads(text[start:end])
    total_count = int(json_obj['count'])
    return total_count


def crawling_overview():
    """
    爬取上市股票概览数据
    """
    num = 60
    url = "http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList['{}']/US_CategoryService.getList?page={}&num=" + num + "&sort=&asc=0&market=&id="
    total_count = get_stock_num(url)
    page_count = math.ceil(total_count / num)
    logger.info(f'total count: {total_count}')
    logger.info(f'page_count: {page_count}')
    total_data = []
    for i in range(page_count):
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        resp = requests.get(url.format(random_str, i + 1))
        if resp.status_code != 200:
            raise RuntimeError(f'response status code:{resp.status_code}')

        text = resp.text.split('\n')[1]
        start = text.find('(') + 1
        end = -2
        json_obj = json.loads(text[start:end])
        data = json_obj['data']
        total_data.extend(data)
        logger.info(f'processing page:{i + 1}')
    return data


def crawling_detail(data):
    """
    爬取个股分时数据
    """
    url = 'https://stock.finance.sina.com.cn/usstock/api/jsonp_v2.php/var%20val=/US_MinlineNService.getMinline?symbol={}&day=1&random={}'
    result = []
    for stock in tqdm(data, total=len(data)):
        symbol = stock['symbol'].lower()
        url = url.format(symbol, round(time.time() * 1000))
        resp = requests.get(url)
        text = resp.text.split('\n')[1]
        start = text.find('(') + 1
        end = -2
        val = text[start:end]
        result.append([symbol, val])
    return result


def get_latest_update_time():
    """
    获取网站数据更新时间
    """
    random_num = int(round(time.time() * 1000))
    url = f'http://hq.sinajs.cn/rn={random_num}&list=gb_dji'
    resp = requests.get(url)
    if resp.status_code != 200:
        raise RuntimeError(f'response status code:{resp.status_code}')
    dt_str = resp.text.split(',')[3]
    dt = datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    return dt


def main():
    logger.info('start crawling.')
    data_path = os.environ.get('DATA_PATH')

    dt = get_latest_update_time().strftime('%Y-%m-%d_%H:%M:%S')
    logger.info(f'data dt:{dt}')
    partition = os.path.join(data_path, dt.split('_')[0])
    if not os.path.exists(partition):
        os.mkdir(partition)

    # 开始爬取数据
    overview_data = crawling_overview()
    detail_data = crawling_detail(overview_data)

    # 保持数据
    overview_file = os.path.join(partition, 'overview.json')
    detail_file = os.path.join(partition, 'detail.d')
    with open(overview_file, 'w+', encoding='utf-8') as f:
        json.dump(overview_data, f, ensure_ascii=False)

    with open(detail_file, 'w+', encoding='utf-8') as f:
        for i in detail_data:
            f.write(f'{i[0]}\1{i[1]}\n')

    logger.info('finish crawling.')


def daemon(do=False):
    """定时器"""
    now = datetime.datetime.now()
    minute = int(now.strftime("%M"))
    hour = int(now.strftime('%H'))
    # 每天早上18点运行
    if hour == 18 and minute == 0:
        main()
    timer = threading.Timer(60, main)
    timer.start()


if __name__ == '__main__':
    main()
