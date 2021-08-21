#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2021/8/21
# CreatTIME : 19:58 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'


REDIS_HOST = '192.168.50.122'
REDIS_PORT = 6380
REDIS_PASSWORD = ''
REDIS_DB = 15
REDIS_TIMEOUT = 888
PROXY_IP_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'  # 代理ip所在的库