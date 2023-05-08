#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import src.util as util
import src.store as store
import time
import jwt
import config

keyPara={
    "data":{
        "require": True,
        "child":{
            "pubkey":{
                "require": True,
            }
        }
    }
}
InfoPara={
    "authorization":{
        "require": True,
    },
    "data":{
        "require": True,
        "child":{
            "user":{
                "comment":"用户字段列表"
            },
            "token":{
                "comment":"token aud列表"
            },
            "pubkey":{
                "comment":"jwt 验签公钥"
            }
        }
    }
}

async def get(account,msg):
    if account:
        return await getInfo(account,msg)
    else:
        return await getPubkey(msg)

#读取jwt 公钥
async def getPubkey(msg):
    util.filter(msg, keyPara)
    with open(config.rsa_public_key,'rb') as fh:
        return {"pubkey":fh.read().decode()}
    
# 用户信息/token获取/jwt公钥
async def getInfo(account,msg):
    para = util.filter(msg, InfoPara)
    fields = para["data"].get("user")
    auds = para["data"].get("token")
    user = store.get(account)
    res = {
        "token": {},
        "user": {},
        "pubkey":""
    }
    if para["data"].get("pubkey"): #读取jwt 公钥
        res.update(getPubkey(msg))
    if fields:  # 查询用户信息
        if type(fields) == str:
            fields = [fields]
        if type(fields) != list:
            fields = user.keys()
        for k in fields:
            res["user"][k] = user.get(k)
    if auds:  # 获取stoken
        instance = jwt.JWT()
        payload = {
            "account": account,
            "name": user.get("name"),
            "icon": user.get("icon"),
            "exp": round(time.time()+config.jwt_exp)
        }
        with open(config.rsa_private_key, 'rb') as fh:
            priKey = jwt.jwk_from_pem(fh.read())
            if type(auds) == str:
                auds = [auds]
            if type(auds) != list:
                auds = [account.split("@")[1]]
            for host in auds:
                payload["aud"] = host
                res["token"][host] = instance.encode(
                    payload, priKey, alg='RS256')
    return res