#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import config
import src.store as store
import src.util as util
from datetime import datetime

pattern = "^(\w)+(\.\w+)*@({})".format("|".join("({})".format(e)
                                                for e in config.host))
# 注册参数
register = {
    "data": {
        "require": True,
        "child": {
            "parent": {
                "comment": "父账户",
                "pattern": "^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$"
            },
            "account": {
                "comment": "账号",
                "required": True,
                "pattern": pattern,
            },
            "pwd": {
                "comment": "密码",
                "required": True,
            },
            "whitelist": {
                "comment": "白名单",
            },
            "blacklist": {
                "comment": "黑名单",
            },
            "router": {
                "comment": "路由",
            },
            "contacts": {
                "comment": "联系人",
            },
            "time": {
                "comment": "注册时间",
                "value": lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    }
}

# 修改参数
edit = {
    "account": {
        "pattern": pattern,
    }
}


# 用户的注册/注销/修改
async def set(account, msg):
    if not account:return add(msg)
    data = msg.get("data")
    if not data: return remove(account)
    util.filter(data, edit) #校验账户格式
    if data.get("account"):
        edit_account = data.pop("account")
    else:
        edit_account=account
    if len(data) == 0: return remove(account)
    # 修改用户信息
    user = store.get(edit_account)
    if not user:
        raise Exception("account error")
    if account != edit_account and account != user.get("parent"):
        raise Exception("Permission Denied")
    user.update(data)
    store.set(account, user)

# 注册
def add(msg):
    if not config.register:
        raise Exception("can not register")
    user = msg.get("data")
    para = util.filter(msg, register)
    user.update(para["data"])  # 合并字典
    if store.get(user["account"]):
        raise Exception("account is registed")
    return store.set(user["account"], user)

# 注销
def remove(account):
    if not config.remove:
        raise Exception("can not remove")
    return store.remove(account)