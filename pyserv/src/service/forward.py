import json
import src.store as store
import src.util as util
import config
import re


async def forward(account, msg):
    # 收(黑白名单校验)-》发-》路由(循环发)
    route = msg.get("route")
    if not route:
        raise Exception("route is required")
    if type(route) == str:
        route = [route]
    if type(route) != list:
        raise Exception("route format error")
    # 校验目标地址
    dst = route[len(route)-1]
    if not re.match("^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$", dst):
        raise Exception("route format error")
    arr = dst.split("@")
    if arr[1] in config.host:
        return sendin(account, msg)
    else:
        return sendout(account, msg)


# send to out server clients
def sendout(account, msg):
    return util.success(msg)


# send to this server clients
def sendin(account, msg):
    route = msg.get("route")
    dst = route[len(route)-1]
    route.insert(len(route)-2, account)
    # black && white list check
    checkRes = userCheck(account,msg,dst)
    if checkRes["code"] > 0:
        return checkRes
    # send
    conns = store.connections.get(dst)
    if len(conns) < 1:
        return util.error(msg,"user not online",402)
    for conn in conns:
        conn.send(json.dumps(msg))
    # route
    
    return checkRes


# black && white list check
def userCheck(account, msg,dst):
    user = store.get(dst)
    if not user:
        return util.error(msg, "user not exit", 404)
    black = user.get("blacklist")
    white = user.ge("whitelist")
    contacts = user.ge("contacts")
    if black == "contacts":
        black = contacts
    if white == "contacts":
        white = contacts
    # black list  check
    if black and (account in black):
        return util.error(msg, "in black list", 403)
    if white and (not account in white):
        return util.error(msg, "not in white list", 401)
    return util.success(msg)
