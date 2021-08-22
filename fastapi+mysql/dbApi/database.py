#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2021/8/21
# CreatTIME : 20:16 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
## 连接数据库

# 连接mysql数据库需要导入pymysql模块
import pymysql

pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .setting import *

# 配置数据库地址：数据库类型+数据库驱动名称://用户名:密码@机器地址:端口号/数据库名
engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}",
                       encoding=MYSQL_ENCODING)
# 把当前的引擎绑定给这个会话；
# autocommit：是否自动提交 autoflush：是否自动刷新并加载数据库 bind：绑定数据库引擎
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 实例化
session = Session()

# declarative_base类维持了一个从类到表的关系，通常一个应用使用一个Base实例，所有实体类都应该继承此类对象
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


