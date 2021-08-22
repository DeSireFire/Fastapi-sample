#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2021/8/21
# CreatTIME : 23:01 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

from sqlalchemy import Column, String, Integer
from .database import Base, engine, session
from pydantic import BaseModel

# 创建数据库模型（定义表结构:表名称，字段名称以及字段类型）
class User(Base):
    # 定义表名
    __tablename__ = 'testUser'
    # 定义字段
    # primary_key=True 设置为主键
    userid = Column(Integer, primary_key=True)
    username = Column(String(255))

    # 构造函数
    def __init__(self, userid, username):
        self.userid = userid
        self.username = username

    # 打印形式
    def __str__(self):
        return "id：%s, name：%s" % (str(self.userid), self.username)

    # 定义返回结果
    def to_dict(self):
        return {
            "userid": self.userid,
            "username": self.username
        }

# 定义数据模型
class CreatUser(BaseModel):
    userid: int
    username: str

    def __str__(self):
        return "id：%s, name：%s" % (str(self.userid), self.username)

# 方式2：
class AlterUser(BaseModel):
    userid: int
    username: str

# 在数据库中生成表
Base.metadata.create_all(bind=engine)



