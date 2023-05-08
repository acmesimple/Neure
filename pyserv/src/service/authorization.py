#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
import jwt
import config as config
import src.store as store

# 授权凭证异常
class AuthorizationExceptin(Exception):
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return self.msg

# 校验用户凭证，失败抛出异常，成功返回账号
def verify(Authorization):
    if not Authorization:return Authorization
    arr = Authorization.split(" ")
    if len(arr) != 2:
        raise AuthorizationExceptin("Authorization format error")

    if arr[0] == "Basic":  # 账号密码认证
        apa = base64.b64decode(arr[1]).decode().split(":")
        if len(apa) != 2:
            raise AuthorizationExceptin("Authorization format error")
        # 校验账号域名
        buff = apa[0].split("@")
        if len(buff) != 2:
            raise AuthorizationExceptin("account format error")
        if not buff[1] in config.host:
            raise AuthorizationExceptin("account error")
        # 校验账号密码
        user = store.get(apa[0])
        if not user:
            raise AuthorizationExceptin("account error")
        if user.get("pwd") != apa[1]:
            raise AuthorizationExceptin("password error")
        return user.get("account")
    if arr[0] == "Bearer":  # Jwt认证
        instance = jwt.JWT()
        with open(config.rsa_public_key, 'rb') as fh:
            pubkey = jwt.jwk_from_pem(fh.read())
            token = instance.decode(arr[1], pubkey, do_time_check=True)
            # 校验aud
            if not token.get("aud") in config.host:
                raise AuthorizationExceptin("jwt aud error")
            account = token.get("account")
            if not account:
                raise AuthorizationExceptin("jwt payload format error")
            if not store.get(account):
                raise AuthorizationExceptin("user is not exist")
            return account
