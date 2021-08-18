#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2021/8/4
# CreatTIME : 17:29 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'


import sys
from redis import Redis, AuthenticationError

from common.logger import logger
from core.config import settings

REDIS_HOST = '192.168.50.122'
REDIS_PORT = 6380
REDIS_PASSWORD = ''
REDIS_DB = 15
REDIS_TIMEOUT = 888
PROXY_IP_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'  # 代理ip所在的库


class RedisCli(object):

    def __init__(self, *, host: str, port: int, password: str, db: int, socket_timeout: int = 5):
        # redis对象 在 @app.on_event("startup") 中连接创建
        self._redis_client = None
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.socket_timeout = socket_timeout

    def init_redis_connect(self) -> None:
        """
        初始化连接
        :return:
        """
        try:
            self._redis_client = Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                db=self.db,
                socket_timeout=self.socket_timeout,
                decode_responses=True  # 解码
            )
            if not self._redis_client.ping():
                logger.info("连接redis超时")
                sys.exit()
        except (AuthenticationError, Exception) as e:
            logger.info(f"连接redis异常 {e}")
            sys.exit()

    # 使实例化后的对象 赋予redis对象的的方法和属性
    def __getattr__(self, name):
        return getattr(self._redis_client, name)

    def __getitem__(self, name):
        return self._redis_client[name]

    def __setitem__(self, name, value):
        self._redis_client[name] = value

    def __delitem__(self, name):
        del self._redis_client[name]


# 创建redis连接对象
# Redis_cli = RedisCli(
#     host=settings.REDIS_HOST,
#     port=settings.REDIS_PORT,
#     password=settings.REDIS_PASSWORD,
#     db=settings.REDIS_DB,
#     socket_timeout=settings.REDIS_TIMEOUT
# )
# 创建redis连接对象
# redis_client: Redis = RedisCli(
Redis_cli = RedisCli(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=REDIS_DB,
    socket_timeout=REDIS_TIMEOUT
)

# 只允许导出 redis_client 实例化对象
# __all__ = ["redis_client"]
