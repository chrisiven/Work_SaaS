#coding:utf-8
import datetime

from django.utils.deprecation import MiddlewareMixin
from users import models
from django.shortcuts import render
from django.shortcuts import redirect,HttpResponseRedirect
from django.conf import settings
from proj.models import Transaction,Project,ProjectUser


class Tracer:

    def __init__(self):
        self.user = None
        self.price_policy = None
        self.project = None

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


    def process_view(self,request,view,args,kwargs):
        """
        当显示项目的一些设置信息时或者项目详细信息时,应该对url进行个判断。
        1.判断该url是否是以manage的形式发起的,如果不是则返回,是则跳转
        2.判断该项目是我创建的还是我参与的.
        :param request:
        :param view:
        :param args:
        :param kwargs:
        :return:
        """

        """
        我理解的思路:
            当我们点击我们项目列表上的一个项目时,浏览器会发送请求到我们的服务器,我们的服务器将请求解析到我们django的中间件
            中间件这边 首先进入的是process_request()，执行完之后,会进入到process_view()。然后我们这边判断浏览器请求的路径是否符合我们的manage规则.
            如果不符合直接返回到项目列表,如果符合则进入到判断中,
            1.判断该项目是"我创建"的还是"我参与"的,符合则进入到相应页面,不符合则返回到项目列表
        """
        if request.path_info.startswith("/manage/"):
            return
        project_id = kwargs.get("project_id")
        my_project = Project.objects.filter(creator=request.tracer.user,id=project_id).first()
        if my_project:
            #是我创建的项目，pass
            request.tracer.project = my_project
            return

        join_project = ProjectUser.objects.filter(user=request.tracer.user,project_id=project_id)
        if join_project:
            # 是我参与的项目，pass
            request.tracer.project = join_project.project
            return
        request.path_info = "/project/list"
        redirect("project:project_list")