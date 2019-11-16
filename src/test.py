import os
import json
import math
import time
import random
import string
import datetime
import requests

url = "http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList['{}']/US_CategoryService.getList?page={}&num=20&sort=&asc=0&market=&id="


def get_total_stock_num():
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


def get_latest_update_time():
    random_num = int(round(time.time() * 1000))
    url = f'http://hq.sinajs.cn/rn={random_num}&list=gb_dji'
    resp = requests.get(url)
    if resp.status_code != 200:
        raise RuntimeError(f'response status code:{resp.status_code}')
    dt_str = resp.text.split(',')[3]
    dt = datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    return dt


def get_all_us_stock():
    total_count = get_total_stock_num()
    page_count = math.ceil(total_count / 20)
    print(f'total count: {total_count}')
    print(f'page_count: {page_count}')
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
        print(f'processing page:{i + 1}')

    dt = get_latest_update_time().strftime('%Y-%m-%d_%H:%M:%S')
    # save
    with open(f'{dt}.json', 'w+', encoding='utf-8') as f:
        json.dump(total_data, f, ensure_ascii=False)


if __name__ == '__main__':
    get_all_us_stock()
