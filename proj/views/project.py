import time

from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from proj.forms.project import ProjectModelForm
from django.views import View
from proj.models import Project,ProjectUser
from users import models
from scripts.Tencent_COS import create_bucket

class ProjectView(View):
    # 1 从数据库中获取两部分的数据
    # 我创建的所有项目, 已星标 未星标
    # 我参与的所有项目  已星标 未星标

    # 2.提取已星标
    # 列表 = 循环 [我创建的所有项目] + [我参与的所有项目] 把已星标的数据提取
    # 然后就得到三个列表

    def get(self,request):
        form = ProjectModelForm(request)
        projects_dict = {"star":[],"my":[],"join":[]}
        my_projects = Project.objects.filter(creator = request.tracer.user)
        my_join_projects = ProjectUser.objects.filter(user=request.tracer.user)
        for proj in my_projects:
            if proj.star:
                projects_dict["star"].append(proj)
            else:
                projects_dict["my"].append(proj)

        for proj in my_join_projects:
            if proj.star:
                projects_dict["star"].append(proj.project)
            else:
                projects_dict["join"].append(proj.project)



        return render(request, "project_list.html", {"forms": form,"project_dict":projects_dict})

    def post(self,request):
        form = ProjectModelForm(request,data=request.POST)
        if form.is_valid():
            # 为项目创建一个桶
            bucket = "{}-{}".format(request.tracer.user.mobile_phone+"-"+form.instance.name,str(int(time.time())))
            region = "ap-nanjing"
            bucket_name = create_bucket(bucket,region)
            form.instance.bucket = bucket_name
            form.instance.creator = request.tracer.user
            request.tracer.user.project_num += 1 #项目数为你添加了多少个项目来进行判断
            request.tracer.user.save() #保存下即可!
            form.save()
            return JsonResponse({"status":True,})

        return JsonResponse({"status":False,"error":form.errors})


def addStar(request):

    proj_id = request.POST.get("addstar")

    result = Project.objects.filter(id=proj_id,creator=request.tracer.user).first()
    if result:
        result.star = True
        result.save()
        return JsonResponse({"status":True})
    return JsonResponse({"status":False})


def cancelStar(request):
    proj_id = request.POST.get("cancelstar")
    result = Project.objects.filter(id=proj_id,creator=request.tracer.user).first()
    if result:
        result.star = False
        result.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})