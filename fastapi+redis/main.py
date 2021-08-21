#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2021/8/4
# CreatTIME : 17:29
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
"""
临时写的玩意，要啥自行车
"""
import uvicorn
import os
import sys
import asyncio
import nest_asyncio

from typing import Optional

from fastapi import FastAPI

from starlette.responses import HTMLResponse

from fastapi import FastAPI, Request, Query

# from dbApi.dbredis import redis_client
from dbApi.dbredis import Redis_cli as redis_client
from fastapi.middleware.cors import CORSMiddleware
nest_asyncio.apply()

def create_app() -> FastAPI:
    """
    生成FatAPI对象
    :return:
    """
    app = FastAPI()
    # 取消挂载在 request对象上面的操作，感觉特别麻烦，直接使用全局的
    register_init(app)

    return app

def register_init(app: FastAPI) -> None:
    """
    初始化连接
    :param app:
    :return:
    """

    @app.on_event("startup")
    async def init_connect():
        # 连接redis
        redis_client.init_redis_connect()

    @app.on_event('shutdown')
    async def shutdown_connect():
        """
        关闭
        :return:
        """
        # 连接redis
        # redis_client.init_redis_connect()
        pass

app = create_app()

@app.get("/redis/add", summary="redis键值对添加")
# 将 Query 用作查询参数的默认值，并将它的 max_length 参数设置为 50：
# async def read_items(q: Optional[str] = Query(None, max_length=50)):
async def test_redis(request: Request,
                     k: Optional[str] = Query("测试用键值对", title="scrapy-redis-key"),
                     v: Optional[str] = Query("数据中台测试api", title="scrapy-redis-value"),
                     m: Optional[str] = Query("set", title="scrapy-redis-mode"),
                     ):

    # 指定存入redis的数据结构
    redis_mode = {
        "str": redis_client.set,
        "list": redis_client.lpush,
        "set": redis_client.sadd,
    }
    status = redis_mode[m](k, v)
    return {"msg": {k: status}}


def run_uvicorn(host="127.0.0.1", port=int(5301)):
    main_app = uvicorn.run(
        app="main:app",
        host=host, port=port,
        reload=True)
    return main_app


if __name__ == '__main__':
    main_app = run_uvicorn()
