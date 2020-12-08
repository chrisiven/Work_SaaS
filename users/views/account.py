#coding:utf-8
import datetime

from django.shortcuts import render,HttpResponse,redirect
# 用户账号管理的功能!
# Create your views here.
from proj.utils.tools import gen_order_id
from django import forms
from users import models
from django.db.models import F,Q
from users.forms.account import RegisterForm,EmailLoginForm,SendEmailCodeForm,LoginForm
from django.views import View
from django.http import JsonResponse
from users.utils.genRandomCodeImage import BigPainter
from proj.models import Transaction,PricePolicy


class RegisterView(View): #注册

    def get(self,request):
        forms = RegisterForm()
        return render(request,"register.html",{"forms":forms})

    def post(self,request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            price_object = PricePolicy.objects.filter(category=1,title="个人免费版").first()

            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            phone = form.cleaned_data.get("mobile_phone")
            pswd = form.cleaned_data.get("password")



            user = models.UserInfo.objects.create(
                username=username,
                email=email,
                password=pswd,
                mobile_phone=phone,
                price_policy=price_object,

            )

            # print("已验证:",form.cleaned_data)

            # instance = form.save()



            Transaction.objects.create(
                    status=1,
                    order_id=gen_order_id(),
                    user=user,
                    price_policy_id= price_object.id,
                    count=0,
                    price=0,
                    start_datetime=datetime.datetime.now()

            )
            return JsonResponse({"status":True})

        return JsonResponse({"status":False,"error":form.errors})




class EmailLoginView(View): #邮箱验证码登录

    def get(self,request):
        forms = EmailLoginForm()
        return render(request, "emaillogin.html", {"forms":forms})

    def post(self,request):

        form = EmailLoginForm(data=request.POST)
        if form.is_valid():
            #将用户信息放入session
            user_obj = form.cleaned_data.get("email","")
            request.session["user_id"] = user_obj.id
            request.session.set_expiry(60*60*24*14)
            return JsonResponse({"status":True})
        return JsonResponse({"status":False,"error":form.errors})



class PswdLoginView(View): #密码登录

    def get(self,request):
        form  = LoginForm(request)
        return render(request,"pswdlogin.html",{"forms":form})

    def post(self,request):
        form = LoginForm(request,data=request.POST)

        if form.is_valid():
            user_email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user_obj = models.UserInfo.objects.filter(Q(email=user_email)|Q(mobile_phone=user_email)).filter(password=password).first()

            if user_obj:
                request.session["user_id"] = user_obj.id
                request.session.set_expiry(60 * 60 * 24 * 14)
                return JsonResponse({"status":True})
            form.add_error("email","用户名或者密码错误")
        return JsonResponse({"status":False,"error":form.errors})



def sendcode(request):
    form = SendEmailCodeForm(request,data=request.POST)
    if form.is_valid():
        return JsonResponse({"status":True,"msg":"验证码发送成功!",})
    return JsonResponse({"status":False,"error":form.errors})

def verify_picture(request):
    from io import BytesIO
    image,code = BigPainter.Draw()
    request.session["image_code"] = None #先初始化...不然会爆KeyError的错误
    request.session["image_code"] = code
    request.session.set_expiry(60)#60s 过期
    stream = BytesIO()
    # print(request.session.get("image_code"))
    image.save(stream,"png")

    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    return redirect("users:pswdlogin")
