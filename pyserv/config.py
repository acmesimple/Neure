import rsa

# 主机域名
host = ["terny.cn", "ternc.cn"]
# data路径
dataDir="./data"
# 开启注册/注销
register = False
remove = False
# jwt公私钥，有效时长
rsa_public_key = "resources/public.pem"
rsa_private_key = "resources/private.pem"
jwt_exp=24*3600


# 生成密钥
def keygen():
    (pubkey,privkey)=rsa.newkeys(1024)
    with open(rsa_private_key,"w+") as f:
        f.write(privkey.save_pkcs1().decode("utf-8"))
    with open(rsa_public_key,"w+") as f:
        f.write(pubkey.save_pkcs1().decode("utf-8"))