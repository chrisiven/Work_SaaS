#coding:utf-8
import datetime

from django.utils.deprecation import MiddlewareMixin
from users import models
from django.shortcuts import redirect
from django.conf import settings
from proj.models import Transaction


class Tracer:

    def __init__(self):
        self.user = None
        self.price_policy = None


class AuthMiddleware(MiddlewareMixin):


    def process_request(self,request):
        """
        如果用户已登录,在request中赋值
        """
        request.tracer = Tracer()

        user_id = request.session.get("user_id",0)
        user_obj = models.UserInfo.objects.filter(id=user_id).first()

        request.tracer.user = user_obj
        """
       1.获取用户当前访问的url,
       2.检查url是否在白名单中,如果在,则继续访问,不在,则进行登录
        """
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return
        if not request.tracer.user :
            return redirect("users:pswdlogin")

        _object = Transaction.objects.filter(user=user_obj,status=1).order_by("-id").first() #查询最新的一条交易记录
        current_datetime = datetime.datetime.now()
        if _object.end_datetime and _object.end_datetime < current_datetime: #如果过期了,那么在显示交易记录的时候直接换为免费版本
            _object = Transaction.objects.filter(user=user_obj,status=1,price_policy__category=1).first() #划分为免费版本

        request.tracer.price_policy = _object.price_policy

