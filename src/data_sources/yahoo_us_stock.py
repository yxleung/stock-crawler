import os
import shutil
import datetime
import pandas as pd
from src.config import logger
from lib import yfinance as yf


def download(dt=None):
    # 设置时区
    os.environ['TZ'] = 'America/New_York'
    yahoo_data_path = os.environ.get('YAHOO_DATA_PATH')
    sina_data_path = os.environ.get('SINA_DATA_PATH')
    if dt is None:
        dt = datetime.datetime.now()
    else:
        dt = datetime.datetime.strptime(dt, '%Y-%m-%d')
    finish_dt = os.listdir(yahoo_data_path)
    total_stocks = pd.read_json(os.path.join(sina_data_path, dt.strftime('%Y-%m-%d'), 'overview.json'))
    total_stocks = total_stocks[['name', 'cname', 'category', 'symbol', 'market']].drop_duplicates(['symbol'],
                                                                                                   keep='first')
    for i in range(30):
        start = (dt + datetime.timedelta(-30 + i)).strftime('%Y-%m-%d')
        end = (dt + datetime.timedelta(-30 + i + 1)).strftime('%Y-%m-%d')
        if start in finish_dt:
            continue
        output_path = os.path.join(yahoo_data_path, start)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        try:
            fout_1m = open(os.path.join(output_path, '1m.d'), mode='a+', encoding='utf-8')
            fout_1d = open(os.path.join(output_path, '1d.d'), mode='a+', encoding='utf-8')

            logger.info(f'================{start}================')
            for j, stock in total_stocks.iterrows():
                t1 = datetime.datetime.now()

                # 下载分钟数据
                df = yf.download(stock['symbol'], start=start, end=end, interval='1m', prepost=True, progress=False,
                                 timeout=600)
                for _, row in df.iterrows():
                    fout_1m.write(
                        f"""{stock['symbol']}\1{row['Open']}\1{row['High']}\1{row['Low']}\1{row['Close']}\1{row[
                            'Adj Close']}\1{row['Volume']}\1{str(row.name)}\n""")
                # 下载天数据
                df = yf.download(stock['symbol'], start=start, end=start, interval='1D', prepost=True, progress=False,
                                 timeout=60)
                for _, row in df.iterrows():
                    fout_1d.write(
                        f"""{stock['name']}\1{stock['cname']}\1{stock['symbol']}\1{stock['category']}\1{stock[
                            'market']}\1{
                        row['Open']}\1{row['High']}\1{row['Low']}\1{row['Close']}\1{row['Adj Close']}\1{row[
                            'Volume']}\1{str(row.name)[0:10]}\n""")
                fout_1d.flush()
                fout_1m.flush()
                t2 = datetime.datetime.now()
                logger.info(
                    f"{stock['symbol']} finish, use {(t2 - t1).total_seconds()} ,processing {j}/{len(total_stocks)}")

            fout_1m.close()
            fout_1d.close()
        except Exception as e:
            shutil.rmtree(output_path)
            logger.exception(e)
            raise RuntimeError(e)


def main():
    download()
