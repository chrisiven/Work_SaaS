#coding:utf-8

from SaaS_System.settings import CODE_EX
from django_redis import get_redis_connection

conn = get_redis_connection("default")


def storageCode_Toredis(email,code,tpl):
    if tpl == "register":
        try:
            result = conn.set(email,code,ex=CODE_EX)
        except Exception as e:
            return False
        if result == True:
            return True
        else:
            return None
    elif tpl == "login":
        try:
            result = conn.set(email, code, ex=CODE_EX) #email:code
        except Exception as e:
            return False
        if result == True:
            return True
        else:
            return None

def getCode_FromRedis(email):
        try:
            result = conn.get(email).decode("utf-8")
        except Exception as e:
            return False
        if result:
            return result
        else:
            return None



def checkEmailCode(email,code:str):
    redis_code = getCode_FromRedis(email)
    if redis_code:

        if str(code) == redis_code:
            print("验证正确!")
            print(email)
        else:
            print("验证错误!")
            print("error!")
    else:
        print("验证码不存在或者已经超时")





if __name__ == '__main__':
    print(storageCode_Toredis("3420@qq.com",3333,"register"))
    checkEmailCode("3420@qq.com",3333)