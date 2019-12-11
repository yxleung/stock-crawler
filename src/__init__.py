import os

# 项目目录
if os.environ.get('PROJECT_HOME') is None:
    PROJECT_HOME = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    os.environ.setdefault("PROJECT_HOME", PROJECT_HOME)

# 数据目录
if os.environ.get('DATA_PATH') is None:
    DATA_PATH = os.path.join(os.environ.get('PROJECT_HOME'), 'data')
    os.environ.setdefault("DATA_PATH", DATA_PATH)
if not os.path.exists(os.environ.get('DATA_PATH')):
    os.makedirs(os.environ.get('DATA_PATH'))

# 新浪财经数据目录
SINA_DATA_PATH = os.path.join(os.environ.get('DATA_PATH'), 'sina')
os.environ.setdefault('SINA_DATA_PATH', SINA_DATA_PATH)
if not os.path.exists(SINA_DATA_PATH):
    os.makedirs(SINA_DATA_PATH)

# yahoo数据目录
YAHOO_DATA_PATH = os.path.join(os.environ.get('DATA_PATH'), 'yahoo')
os.environ.setdefault('YAHOO_DATA_PATH', YAHOO_DATA_PATH)
if not os.path.exists(YAHOO_DATA_PATH):
    os.makedirs(YAHOO_DATA_PATH)
