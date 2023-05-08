#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import config
_set=set
'基于文件的数据存储器'
__author__ = 'TeRny'

# 用户连接
connections={}

def getConn(k):
    global connections
    if not k:return False
    return connections.get(k)
def addConn(k,ws):
    global connections
    if not k:return False
    if not connections.get(k):connections[k]=_set()
    return connections[k].add(ws)
def delConn(k,ws):
    global connections
    if not k:return False
    if not connections.get(k):return False
    return connections[k].remove(ws)

# 用户数据
data = {}
path=config.dataDir
def get(k):
    global data
    if not k:return False
    res=data.get(k)
    return res.copy() if res else None

def set(k,v):
    global data
    if not k:return False
    a=k.split("@")
    if len(a)!=2:return False
    if data.get(k)==v:return True
    data[k]=v
    # data Persistence
    dir=os.path.join(path,a[1])
    file=os.path.join(dir,a[0]+".json")
    if not os.path.isdir(dir):os.makedirs(dir)
    with open(file,"w") as f:json.dump(v,f,indent="\t",ensure_ascii=False)
    return True

def remove(k):
    global data
    if not k:return False
    a=k.split("@")
    if len(a)!=2:return False
    if not data.get(k):return True
    # remove
    file=os.path.join(path,a[1],a[0]+".json")
    os.remove(file)
    del data[k]
    return True

# load data from disk
def load():
    global data
    data={}
    if not os.path.isdir(path):
        os.makedirs(path)
    hosts=os.listdir(path)
    for host in hosts:
        dir=os.path.join(path,host)
        if not os.path.isdir(dir):continue
        files=os.listdir(dir)
        for file in files:
            d=os.path.join(dir,file)
            if not os.path.isfile(d):continue
            user=file.replace(".json","")
            key=user+"@"+host
            with open(d) as f:
                data[key]=json.load(f)

load()