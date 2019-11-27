#!/usr/bin/env bash

docker run \
    --name stock-crawler \
    -v /nas/xiaomi/projects/stock/logs:/opt/project/logs \
    -v /nas/xiaomi/projects/stock/data:/opt/project/data \
    -d \
    --restart=always \
    --dns 114.114.114.114 \
    yxleung/stock-crawler
