FROM yxleung/ubuntu:18.04.2_python3.7.4

LABEL maintainer="liangyuxin.02@gmail.com"

# 设置时区
RUN apt-get install tzdata
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo "Asia/Shanghai" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PROJECT_HOME=/opt/project
ENV PYTHON_HOME=/opt/python3.7.4
ENV PATH=$PROJECT_HOME:$PYTHON_HOME/bin:$PATH
ENV PYTHONPATH=$PROJECT_HOME
ENV DATA_PATH=$PROJECT_HOME/data
ENV LOG_PATH=$PROJECT_HOME/logs

COPY . $PROJECT_HOME
WORKDIR $PROJECT_HOME

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt

ENTRYPOINT ["python3.7","src/us_stock.py"]
