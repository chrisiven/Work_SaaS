#coding:utf-8
from django.template import Library
from django.urls import reverse
from proj import models


register = Library()
@register.inclusion_tag("inclusion/all_projec_list.html")
def all_project_list(request):
    my_creater_project = models.Project.objects.filter(creator=request.tracer.user)
    my_join_project = models.ProjectUser.objects.filter(user=request.tracer.user)

    return {"my_project":my_creater_project,"join_project":my_join_project,"request":request}

@register.inclusion_tag("inclusion/manage_menu_list.html")
def manage_menu_list(request):
    data_list = [
        {"title":"概览","url":reverse("project:dashboard",kwargs={"project_id":request.tracer.project.id})},
        {"title": "问题", "url": reverse("project:issues", kwargs={"project_id": request.tracer.project.id})},
        {"title": "wiki", "url": reverse("project:wiki", kwargs={"project_id": request.tracer.project.id})},
        {"title": "统计", "url": reverse("project:statistics", kwargs={"project_id": request.tracer.project.id})},
        {"title":"文件","url":reverse("project:file",kwargs={"project_id":request.tracer.project.id})},
        {"title": "配置", "url": reverse("project:setting", kwargs={"project_id": request.tracer.project.id})}

    ]
    for item in data_list:
        if request.path_info.startswith(item["url"]):
            item["class"] = "active"
    return {"data_list":data_list}
