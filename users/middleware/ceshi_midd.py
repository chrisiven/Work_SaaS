#coding:utf-8

from django.utils.deprecation import MiddlewareMixin


class Ceshi_midd(MiddlewareMixin):

    def process_request(self,request):
        # print("我是process_request")
        request
        pass
        return

    def process_view(self,request,view,args,kwargs):
        # print("我是process_view")
        request
        return