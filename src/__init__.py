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
