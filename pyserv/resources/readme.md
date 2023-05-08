### 消息结构
```js
var msg={
    id:"msg uuid",//消息id
    type:"get/set/message",//【请求/响应】
    authorization:"",//用户凭证，【请求】
    path:[from,broker,to],//网络路径
    data:{

    },//【请求/响应】
    code:0,//状态码，【响应】
    time:"",//【请求/响应】
}
```
### authorization类型
- jwt token
    支持rs256 非对称签名的jwt token。
    格式 "authorization: Bearer token_str"
- http basic
    "authorization: Basic base64(account:pwd).toString()"

### 系统消息类型
- sys/get
    获取token、用户信息、签名公钥
    ```js
        {
            type:"get",
            authorization:"",
            data:{
                user:true, //获取用户信息。需授权。可指定字段，例 user:["contacts","icon","name"]
                token:true,//获取token。需授权。可获取对特定主机的授权，例 token:["baidu.com","sina.com"]
                pubkey:true,//获取签名公钥。无需授权
            }
        }
        
    ```
- sys/set
    - 添加用户： 无authorization，状态下为注册用户信息
    - 注销用户： 有authorization，data数据仅有 account.
    - 修改用户信息：有authorization，有除account之外要修改的字段。支持多维度修改


- sys/error
    系统错误

### 用户字段
```js
obj={
    // 固定字段
    "parent": "父账户",
    "account": "账户",
    "pwd": "密码",
    "whitelist": "白名单",
    "blacklist": "黑名单",
    "router": "路由",
    "contacts": [
        {
            "account": "账户",
            "nickname": "备注名",
        }
    ],//联系人
    "name": "姓名",
    "icon": "头像",
    "time": "注册时间",
    // 其他任意自定义字段
}
```
- 账户规则 等同于 邮件账户