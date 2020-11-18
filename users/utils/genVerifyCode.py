#coding:utf-8

from SaaS_System.local_settings import *
from random import randint
from redis import Redis


red = Redis(host=REDIS_HOST,password=REDIS_PASSWORD,port=REDIS_PORT,db=REDIS_DB)

def generate_registercode():#验证码:注册
    code = randint(1,1000000)
    print(code)
    result = red.set("registercode",code,ex=60)
    if result:
        return True
    else:
        return False

def generate_logincode():#登录验证码
    code = randint(1,10000)
    print(code)
    result = red.set("logincode", code, ex=60)
    if result:
        return True
    else:
        return False




if __name__ == '__main__':
    print(generate_registercode())
    print(generate_logincode())