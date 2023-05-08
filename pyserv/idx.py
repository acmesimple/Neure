#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from websockets import serve
import asyncio
import json
import traceback
import src.store as store
import src.util as util
import src.service.authorization as authorization
import src.service.get as serviceGet
import src.service.set as serviceSet
import src.service.forward as serviceForward
# 消息格式校验
msgPara = {
    "id": {"required": True},
    "type": {"required": True},
    "authorization": {"pattern": "^(Basic)|(Bearer) \S*"},
}
#连接处理程序
async def handler(ws):
    account = ""
    async for msg in ws:
        try:
            msg = json.loads(msg)
            util.filter(msg, msgPara)
            action = msg.get("type")
            account = authorization.verify(msg.get("authorization"))
            if account:store.addConn(account, ws)    # 添加用户链接
            res = "success"
            if action == "sys/get":
                res = await serviceGet.get(account, msg)
            elif action == "sys/set":
                await serviceSet.set(account, msg)
            else:
                await serviceForward.forward(account, msg)
            await ws.send(json.dumps(util.success(msg, res)))
        except Exception as e:
            traceback.print_exc()
            traceback.format_exc()
            data = e.__dict__.get("data")
            if not data:data = str(e)
            if not msg:msg = {}
            data = json.dumps(util.error(msg, data))
            return await ws.send(data)
    # 移除用户链接
    await ws.wait_closed()
    store.delConn(account, ws)

# websocket 服务器
async def start(port=35, ip=''):
    async with serve(handler, ip, port):  # ,ping_interval=3
        await asyncio.Future()

asyncio.run(start())
