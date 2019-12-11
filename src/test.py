import datetime
import time as _time
import os
from lib import yfinance as yf

os.environ['TZ'] = 'America/New_York'

start = datetime.datetime.strptime('2019-12-10', '%Y-%m-%d')
end = datetime.datetime.strptime('2019-12-11', '%Y-%m-%d')

print(start)
print(start.timestamp())
print(int(_time.mktime(start.timetuple())))

print(end)
print(end.timestamp())

# d = yf.download(['BABA'], start=start, end=end, interval='1m', prepost=True,timeout=60)
df = yf.download('BABA', start=start, end=end, interval='1D', prepost=True, progress=False,
                 timeout=60)
print(df)
