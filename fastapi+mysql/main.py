#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2021/8/21
# CreatTIME : 20:15 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

# 导入FastAPI模块
from fastapi import FastAPI
from dbApi.model import CreatUser, User, session, AlterUser
from sqlalchemy.exc import IntegrityError
# 创建app实例
app = FastAPI()

## 添加单个
@app.post("/user/addUser")
async def InserUser(user: CreatUser):
    try:
        # 添加数据
        dataUser = User(userid=user.userid, username=user.username)
        session.add(dataUser)
        session.commit()
    except ArithmeticError:
        session.rollback()
        return {"code": "0002", "message": "数据库异常"}
    except IntegrityError:
        session.rollback()
        return {"code": "0002", "message": "数据重复"}
    finally:
        session.close()
    return {"code": "0000", "message": "添加成功"}


from typing import List

## 添加多个
@app.post("/user/addUserList")
async def addUserList(*, user: List[CreatUser]):
    try:
        # user是一个列表，每个内部元素均为CreatUser类型
        for u in user:
            # 自定义的数据模型可以用.访问属性
            dataUser = User(userid=u.userid, username=u.username)
            session.add(dataUser)
        session.commit()
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return {"code": "0000", "message": "添加成功"}


### 查询

## 按照user_id查询192.168.56.20
@app.get("/user/{user_id}")
async def queryUserByUserId(user_id: int):
    # 创建Query查询，filter是where条件，调用one返回唯一行，调用all则是返回所有行
    try:
        # one与first的区别：
        # one：要求结果集中只有一个结果；如果数据库返回0或2个或更多结果，并且将引发异常，则为错误。
        # first：返回可能更大的结果集中的第一个，如果没有结果，则返回None。不会引发异常。
        # filter_by与filter的区别：
        # filter_by接收的参数形式是关键字参数，而filter接收的参数是更加灵活的SQL表达式结构
        # user1 = session.query(User).filter_by(userid=user_id).first()
        user1 = session.query(User).filter(User.userid == user_id).first()
        session.close()
        # 由于user1只有一个值，所以它直接是一个字典
        if user1:
            return {"code": "0000", "message": "请求成功", "data": user1}
        else:
            return {"code": "0001", "message": "查询无结果"}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}


## 查询所有
@app.get("/user/selectall/")
async def queryUserByUserId():
    # 创建Query查询，filter是where条件，调用one返回唯一行，调用all则是返回所有行
    try:
        user1 = session.query(User).all()
        session.close()
        # user1 是一个列表，内部元素为字典
        return {"code": "0000", "message": "请求成功", "data": user1}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}


###删除

# 根据user_id删除单个
@app.delete("/user/deleteUser/{user_id}")
async def deleteUser(user_id: int):
    try:
        user1 = session.query(User).filter(User.userid == user_id).first()
        if user1:
            session.delete(user1)
            session.commit()
            session.close()
            return {"code": "0000", "message": "删除成功"}
        else:
            return {"code": "0001", "message": "参数错误"}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库错误"}


from typing import List


## 删除多个
@app.delete("/user/deleteUserList")
async def deleteUser(user_ids: List[int]):
    try:
        for user_id in user_ids:
            user1 = session.query(User).filter(User.userid == user_id).first()
            if user1:
                session.delete(user1)
                session.commit()
                session.close()
        return {"code": "0000", "message": "删除成功"}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库错误"}


###修改

## 根据user_id修改user_name
@app.put("/user/updateUser/")
# 定义查询参数user_id和user_name
async def updateUser(user_id: int, user_name: str):
    try:
        user1 = session.query(User).filter(User.userid == user_id).first()
        print(user1)
        if user1:
            user1.username = user_name
            session.commit()
            session.close()
            return {"code": "0000", "message": "修改成功"}
        else:
            return {"code": "0001", "message": "参数错误"}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库错误"}





@app.put("/user/updateUser01/")
async def deleteUser(user: AlterUser):
    try:
        user1 = session.query(User).filter(User.userid == user.userid).first()
        if user1:
            user1.username = user.username
            session.commit()
            session.close()
            return {"code": "0000", "message": "修改成功"}
        else:
            return {"code": "0001", "message": "参数错误"}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库错误"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host="127.0.0.1", port=8000, debug=True)
