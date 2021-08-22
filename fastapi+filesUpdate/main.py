#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2021/8/21
# CreatTIME : 20:15
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
from typing import List
import uvicorn
import time

from fastapi import FastAPI, File, UploadFile
from starlette.responses import HTMLResponse

app = FastAPI()


# file: bytes = File(...),            # 把文件对象转为bytes类型，这种类型的文件无法保存
# fileb: UploadFile = File(...),      # UploadFile转为文件对象，可以保存文件到本地
# notes: str = Form(...)              # 获取普通键值对

@app.post("/file/")
async def create_files(file: bytes = File(...)):
    with open('./base.jpg', 'wb') as f:
        f.write(file)

    return {"fileSize": len(file)}


@app.post('/uploadFile')
async def uploadFile(file: UploadFile = File(...)):
    """缺少验证是否上传文件"""
    content = await file.read()
    with open('./test.jpg', 'wb') as f:
        f.write(content)

    return {"filename": file.filename}


@app.post("/files/")
async def create_files(
        files: List[bytes] = File(...)
):
    print(type(files))
    print(files)
    for i in files:
        with open(f'./{time.time()}.jpg', 'wb') as f:
            f.write(i)

    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(
        files: List[UploadFile] = File(...)
):
    for i in files:
        content = await i.read()
        if content:
            print(content)
            with open(f'./{time.time()*1000}.jpg', 'wb') as f:
                f.write(content)

    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
    <body>
    <form action="/file/" enctype="multipart/form-data" method="post">
    <input name="file" type="file">
    <input type="submit" value="file上传">
    </form>
    <form action="/files/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit" value="files上传">
    </form>
    <form action="/uploadFile/" enctype="multipart/form-data" method="post">
    <input name="file" type="file">
    <input type="submit" value="uploadFile上传">
    </form>
    <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit" value="uploadfiles上传">
    </form>
    </body>
     """
    return HTMLResponse(content=content)


if __name__ == '__main__':
    uvicorn.run(app)
