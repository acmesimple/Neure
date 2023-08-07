#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from inspect import isfunction
import re


def success(msg,data="success",code=0):
    return {
        "id":msg.get("id"),
        "type":msg.get("type"),
        "code":code,
        "data":data,
        "time":round(time.time())
    }
    
def error(msg,data="fail",code=1):
    return success(msg,data,code)


# 校验异常
class ValidateException(Exception):
    def __init__(self,msg):
        self.msg=msg
    def __str__(self):
        return self.msg

#根据规则校验数据格式。未实现数组以及数组元素格式校验
def filter(para,rule,parent=False):
    class Error:
        data={}
        flag=False
        def add(self,k,v):
            self.flag=True
            if not self.data.get(k):
                self.data[k]=[]
            self.data[k].append(v)
    err=Error()
    obj={}
    for k in rule:
        field=rule[k].get("comment") if rule[k].get("comment") else k
        if parent:field=parent+"."+field
        # set default value
        defVal=rule[k].get("default")
        if isfunction(defVal):defVal=defVal()
        val=rule[k].get("value")
        if isfunction(val):val=val()
        if defVal != None:obj[k]=defVal
        if para.get(k)!=None:obj[k]=para.get(k)
        if val !=None:obj[k]=val

        # required validate
        if rule[k].get("required") and obj.get(k)==None:
            err.add(k,"{} required".format(field))
        if obj.get(k)==None:continue
        # dict validate
        dc=rule[k].get("dict")
        if dc:
            if isfunction(dc):dc=dc()
            if type(dc)==dict:dc=dc.keys()
            if type(dc)!=list:raise Exception("{} dict error".format(k))
            if not obj[k] in dc:err.add(k,"{} not in dict".format(field))
        # RegExp validate
        patt=rule[k].get("pattern")
        if patt:
            if not re.match(patt,obj[k]):
                err.add(k,"{} format error".format(field))
        # validate children
        child=rule[k].get("child")
        if child:obj[k]=filter(obj[k],child,field)
        
    if err.flag:
        e=ValidateException("filter error")
        e.data=err.data
        raise e
    return obj

