jwt:{
    aud:"受众",
    account:"",
    name:"",
    icon:"",
    exp:"过期时间"
}
收-》发-》路由
收：
    校验aud->jwt验签->黑白名单校验
    

用户
    账号    account
    
    父账户  parent
    密码    pwd
    白名单  receive 联系人/没有/自定义
    黑名单  refuse 自定义/没有
    路由   router
    
    联系人  contacts
        账号 备注
    昵称    name
    头像    icon
    时间    time

    其他    meta
        主页
        铃声
        手机号
        app

消息
    id
    来源ID
    发送着 sender
    接收者  reciver
    来源    source
    消息类型    type
    消息内容    content
    时间    time

例如 a->b->c->d
来源 a->b
发送者 c
接收者 d


注册-》注销-》登录-》修改用户信息-》发消息
注册响应-》注销响应-》登录响应-》修改响应-》

{
    token:"",
    type:"",
    router:[],
    content:{

    },
    time:""
}

app
    用户
    名称
    图标
    地址
    时间

