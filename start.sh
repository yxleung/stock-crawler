#!/usr/bin/env bash

docker run \
    --name stock-crawler \
    -v /home/lyx/projects/stock/logs:/opt/project/logs \
    -v /home/lyx/projects/stock/data:/opt/project/data \
    -d \
    --restart=always \
    --dns 114.114.114.114 \
    yxleung/stock-crawler
