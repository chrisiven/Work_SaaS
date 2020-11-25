#coding:utf-8

from django import forms
from users import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .base_bootstrap import Base_Bootstrap
from users.utils.redisTool import storageCode_Toredis,getCode_FromRedis
from users.utils.sendCode import send_EmailCode
from users.utils.timeManager import oneHourMaxClickNumber
import random
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password



class RegisterForm(Base_Bootstrap):


    password = forms.CharField(label="密码",
       min_length=8,
       max_length=16,
       error_messages={
        "min_length":"密码长度不能小于8位",
        "max_length":"密码长度不能大于16位"
    },widget=forms.PasswordInput())

    confirm_password = forms.CharField(label="重复密码",
       min_length=8,
       max_length=16,
       error_messages={
        "min_length":"重复密码长度不能小于8位",
        "max_length":"密码长度不能大于16位"
    },widget=forms.PasswordInput())
    mobile_phone = forms.CharField(label="手机号", validators=[RegexValidator(r'(1[3|4|5|6|7|8|9]\d{9})', "手机号格式错误"), ])  # 走正则表达式
    code = forms.CharField(label="验证码", widget=forms.TextInput())


    class Meta:
        model = models.UserInfo
        fields = ["username","email","mobile_phone","password","confirm_password","code"]
        # fields = ["mobile_phone",]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        exists = models.UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError("用户名已存在")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        exists = models.UserInfo.objects.filter(email=email).exists()

        if exists:
            raise ValidationError("邮箱已存在")
        return email

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get("mobile_phone")
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError("手机号已注册")
        if len(mobile_phone) < 11 or len(mobile_phone) >11:
            raise ValidationError("手机号码不对哦~")
        return mobile_phone

    def clean_password(self):
        pswd = self.cleaned_data.get("password","")

        encrytion_paswd = make_password(pswd,"pbkdf2_sha256")
        # print(" in password",encrytion_paswd)
        return encrytion_paswd

    def clean_confirm_password(self):
        pswd = self.cleaned_data.get("password","")
        confirm_pswd = self.cleaned_data.get("confirm_password","")
        encrytion_confirm_pswd = make_password(confirm_pswd,"pbkdf2_sha256")

        #如果要校验confirm_password 那么
        if pswd != encrytion_confirm_pswd:
            raise ValidationError("两次密码不一致")
        # print("in confirm_password",encrytion_confirm_pswd)
        return encrytion_confirm_pswd


    def clean_code(self):
        code = self.cleaned_data.get("code","")
        email = self.cleaned_data.get("email","")
        #验证邮箱验证码

        redis_code = getCode_FromRedis(email)
        if not redis_code:
            raise ValidationError("验证码失效,请重新发送~")

        if code.strip() != redis_code:
            raise ValidationError("验证码错误")

        return code




class SendEmailCodeForm(forms.Form):#验证码模块

    email = forms.EmailField(label="邮箱")

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request

    def clean_email(self):
        no_valid_email = self.cleaned_data.get("email")
        # exists = models.UserInfo.objects.filter(email=no_valid_email).exists()

        # if exists:
        #     # self.add_error() 两者报错一样 这个报错了下面的还会继续执行
        #     raise ValidationError("邮箱已经存在")#这个出错了就会抛出异常 不会执行下面的动作


        #如果不对邮箱进行验证的话会出现什么情况呢？
        #
        # 1.用户在注册的时候，邮箱本来就是不存在的
        # 2.用户在登录的时候,如果邮箱不存在那么直接跳到注册页面即可!

        result = oneHourMaxClickNumber(no_valid_email+"_")
        if result == True:#一个小时内最大的点击次数

            code = random.randrange(10000,99999)
            tpl = self.request.POST.get("tpl")
            if tpl == "register":
                result = storageCode_Toredis(no_valid_email,code,tpl=tpl) #存储生成的验证码在数据库
                if result == True:
                    send_EmailCode(no_valid_email,code,tpl)
            elif tpl == "login":
                result = storageCode_Toredis(no_valid_email, code, tpl=tpl)  # 存储生成的验证码在数据库
                if result == True:
                    send_EmailCode(no_valid_email, code, tpl)
        else:
            raise ValidationError("对不起,您在一个小时内发送的请求过多,请稍后重试")
        return no_valid_email



class EmailLoginForm(Base_Bootstrap,forms.Form): # 登录
    email = forms.EmailField(label="邮箱",widget=forms.EmailInput())
    code = forms.CharField(label="验证码",widget=forms.TextInput())

    class Meta:
        model = models.UserInfo
        fields = ["email","code"]


    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_obj = models.UserInfo.objects.filter(email=email) #直接返回这个对象，省一次查询
        if user_obj.exists():
            return user_obj.first()
        raise ValidationError("邮箱不存在，请前往注册")

    def clean_code(self):
        no_virify_code = self.cleaned_data.get("code")
        user_obj = self.cleaned_data.get("email")
        if not user_obj:
            raise ValidationError("用户不存在,请重新注册")
        # 多层捕捉错误,提高程序的容错率和健壮性
        code = getCode_FromRedis(user_obj.email)
        if no_virify_code != code:
            raise ValidationError("验证码错误")
        return code



class LoginForm(Base_Bootstrap,forms.Form):

    email = forms.CharField(label="手机号或邮箱")

    password = forms.CharField(label="密码",
                               min_length=8,
                               max_length=16,
                               error_messages={
                                   "min_length": "密码长度不能小于8位",
                                   "max_length": "密码长度不能大于16位"
                               }, widget=forms.PasswordInput())
    code = forms.CharField(label="图片验证码", widget=forms.TextInput())


    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)#
        self.request = request

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if len(email) == 11 :
            result = models.UserInfo.objects.filter(mobile_phone=email).exists()
            if result :
                return email
            raise ValidationError("手机号不存在,请返回注册")
        elif "@" in email:
            result = models.UserInfo.objects.filter(email=email).exists()
            if result:
                return email
            raise ValidationError("邮箱不存在,请返回注册")

    def clean_password(self):

        pswd = self.cleaned_data.get("password")
        userpswd =  make_password(pswd,"pbkdf2_sha256")

        return userpswd


    def clean_code(self):

        code = self.cleaned_data.get("code")
        session_code = self.request.session.get("image_code")
        if not session_code:
            raise ValidationError("验证码已过期，请重新获取")
        if code.strip().upper() != session_code.strip().upper():
            raise ValidationError("验证码输入错误")

        return code
