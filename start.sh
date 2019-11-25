#!/usr/bin/env bash

docker run \
    --name stock-crawler \
    -v /data/xiaomi/projects/stock/logs:/opt/project/logs \
    -v /data/xiaomi/projects/stock/data:/opt/project/data \
    -d \
    --restart=always \
    yxleung/stock-crawler
