const fs=require("fs")
const path=require("path")

class Store{
    data={}
    constructor(path="./data"){
        try{
            var exist=fs.lstatSync(path).isDirectory()
        }catch(e){
            var exist=false
        }
        if(!exist)fs.mkdirSync(path,{recursive:true})
        this.path=path
        this.load()
    }
    get=k=>this.data[k]
    set(k,v){
        var a=k.split("@")
        if(a.length!=2)return false
        if(this.data[k]==v)return true
        this.data[k]=v
        //持久化
        var json=JSON.stringify(this.data[k],null,"\t")
        var file=path.join(this.path,`${a[1]}/${a[0]}.json`)
        this.writeFile(file,json)
    }
    del=k=>{
        var a=k.split("@")
        if(a.length!=2)return false
        if(!this.data[k])return false
        delete this.data[k]
        // 删除文件
        var file=path.join(this.path,`${a[1]}/${a[0]}.json`)
        fs.promises.unlink(file)
    }
    //加载数据到内存
    load(){
        var hosts=fs.readdirSync(this.path)
        for(var i in hosts){
            var dir=path.join(this.path,hosts[i])
            if(!fs.lstatSync(dir).isDirectory())continue
            var files=fs.readdirSync(dir)
            for(var k in files){
                var d=path.join(this.path,hosts[i],files[k])
                if(!fs.lstatSync(d).isFile())continue
                var user=files[k].replace(".json","")
                var key=`${user}@${hosts[i]}`
                var json=fs.readFileSync(d)
                this.data[key]=JSON.parse(json)
            }
        }
    }
    //写文件
    async writeFile(file,data){
        var dir=path.dirname(file)
        await fs.promises.access(dir).catch(async err=>{
            await fs.promises.mkdir(dir,{recursive:true})
            fs.promises.writeFile(file,data)
        })
        fs.promises.writeFile(file,data)
    }
}
module.exports=Store