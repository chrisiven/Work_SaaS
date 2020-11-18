#coding:utf-8
from django.core.mail import send_mail

from SaaS_System.settings import EMAIL_HOST,EMAIL_HOST_USER



def send_EmailCode(to_email:str,code,tpl:str):#发送邮箱验证码
    if tpl == "register":
        send_object_title = "天问SaaS系统注册邮箱验证码"
        send_object_content = "您好,欢迎您入驻天问SaaS系统,您的邮箱验证码为:{}".format(code)
        send_from_email = EMAIL_HOST_USER
        try:
            result = send_mail(send_object_title, send_object_content, send_from_email, [to_email,], fail_silently=False)
        except Exception as e:
            return {"send_type": False, "code": 0,"tpl":"register","errors":e}
        if result == 1 or result == "1":
            print("发送成功~")
            return {"send_type":True,"code":1,"tpl":"register"}
        else:
            print("发送失败~")
            return {"send_type":False,"code":0,"tpl":"register"}

    elif tpl == "login":
        send_object_title = "天问SaaS系统登录邮箱验证码"
        send_object_content = "您好,您的邮箱登录验证码为:{}".format(code)
        send_from_email = EMAIL_HOST_USER
        try:
            result = send_mail(send_object_title, send_object_content, send_from_email, [to_email, ], fail_silently=False)
        except Exception as e:
            return {"send_type": False, "code": 0,"tpl":"login","errors":e}

        if result == 1 or result == "1":
            print("发送成功~")
            return {"send_type": True, "code": 1,"tpl":"login"}
        else:
            print("发送失败~")
            return {"send_type": False, "code": 0,"tpl":"login"}
    else:
        raise Exception("未知错误~")# 添加一个Log系统

if __name__ == '__main__':

    # send_EmailCode("342083472@qq.com","22334","register")
    pass