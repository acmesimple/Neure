class Neure {
    constructor(url) {
        this.url = url
        this.e = new EventTarget()
        // 读取持久化数据
        var user=localStorage.getItem("__neure_user")
        this.user=user?JSON.parse(user):null
        this.connect()
    }
    async connect() {
        return await new Promise(resolve => {
            var socket = new WebSocket(this.url)
            this.socket = socket
            socket.onopen = e => resolve(e)
            socket.onclose = e => this.socket = null
            socket.onmessage = e => {
                var msg = JSON.parse(e.data)
                var event = new Event(msg.type)
                event.data = msg
                this.e.dispatchEvent(event)
            }
        })
    }
    uuid() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8)
            return v.toString(16)
        })
    }
    getTime(str) {
        var date = str ? new Date(str) : new Date();
        return Math.round(date.getTime() / 1000);
    }
    getDate(time, fmt = 'YY-m-d h:i:s') {
        var date = time ? new Date(time * 1000) : new Date();
        var map = {
            "(y+)": `${date.getFullYear()}`,
            "(m+)": `0${date.getMonth() + 1}`.slice(-2),
            "(d+)": `0${date.getDate()}`.slice(-2),
            "(h+)": `0${date.getHours()}`.slice(-2),
            "(i+)": `0${date.getMinutes()}`.slice(-2),
            "(s+)": `0${date.getSeconds()}`.slice(-2),
        }
        for (var i in map) {
            if (new RegExp(i, 'i').test(fmt))
                fmt = fmt.replace(RegExp.$1, map[i].substr(-2 * RegExp.$1.length))
        }
        return fmt;
    }
    // 不携带token,发送消息
    async sent(msg) {
        if (!this.socket) await this.connect()
        return new Promise(resolve => {
            this.socket.send(JSON.stringify(msg))
            this.e.addEventListener(msg.type, e => resolve(e.data), { once: true })
        })
    }
    // 携带token,发消息
    async send(type,data){
        var msg={
            id:this.uuid(),
            type:type,
            data:data,
            time:this.getTime()
        }
        if(this.user&&this.user.token)
            msg.authorization="Bearer "+this.user.token
        return await this.sent(msg)
    }
    // 接收消息
    async on(type,fun,once=false){
        this.e.addEventListener(type,fun,{once})
    }
    // 修改用户数据
    async setUser(data){
        if(!data)return false
        var res=await this.send("sys/set",data)
        if(res.code)return false
        Object.assign(this.user,data)
        localStorage.setItem("__neure_user",JSON.stringify(this.user))
        return this.user
    }
    // 登录
    async login(para) {
        if (!para.account || !para.pwd) return alert("Please enter you account and password~")
        var token = `Basic ${btoa(para.account + ':' + para.pwd)}`
        var msg = {
            id: this.uuid(),
            type: "sys/get",
            authorization: token,
            data: { token: true, user: true }
        }
        var res = await this.sent(msg)
        if(res.code)return res
        this.user=res.data.user
        this.user.token=Object.values(res.data.token)[0]
        localStorage.setItem("__neure_user",JSON.stringify(this.user))
        return res
    }
}