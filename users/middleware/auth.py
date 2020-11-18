#coding:utf-8


from django.utils.deprecation import MiddlewareMixin
from users import models


class AuthMiddleware(MiddlewareMixin):


    def process_request(self,request):
        """
        如果用户已登录,在request中赋值
        """
        user_id = request.session.get("user_id",0)
        user_obj = models.UserInfo.objects.filter(id=user_id).first()
        if user_obj:
            request.tracer = user_obj
