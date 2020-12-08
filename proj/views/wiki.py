#coding:utf-8

from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from proj.forms.wiki import WikiModelForm
from django.urls import reverse
from django.http import JsonResponse
from proj.models import Wiki
from scripts.Tencent_COS import upload_file
import string
from scripts.encrypt import uid

from django.views.decorators.csrf import csrf_exempt

def wiki_delete(request,project_id,del_id):

    if del_id:
        obj = Wiki.objects.filter(project_id=project_id,id=del_id).delete() #删除当前id内的wiki问题
        url = reverse("project:wiki", kwargs={"project_id": project_id})
        return redirect(url)


class EditWiki(View):



    def get(self,request,project_id,wiki_id):
        wiki_object = Wiki.objects.filter(project_id=project_id, id=wiki_id).first()  # 删除当前id内的wiki问题

        if not wiki_object:
            url = reverse("project:wiki", kwargs={"project_id": project_id})
            return redirect(url)
        form = WikiModelForm(request,instance=wiki_object)


        return render(request, "wiki_form.html", {"form":form})

    def post(self,request,project_id,wiki_id): #是因为需要修改然后就必须传递修改后的内容 所以instance所扮演的角色就是一个传递内容的容器.传递过去后
        #代替原有的或者没有的内容/
        wiki_object = Wiki.objects.filter(project_id=project_id, id=wiki_id).first()
        if not wiki_object:
            url = reverse("project:wiki", kwargs={"project_id": project_id})
            return redirect(url)
        form = WikiModelForm(request,data=request.POST,instance=wiki_object) # instance 可以说是结构化的数据相当于 QuerySet!
        if form.is_valid():

            if form.instance.parent:
                form.instance.depth = form.instance.parent.depth+1 #二级标签是父类的深度+自己的深度等于第三个深度
            else:
                form.instance.depth = 1
            form.save()
            url = reverse("project:wiki",kwargs={"project_id":project_id})
            preview_url = "{0}?wiki_id={1}".format(url,wiki_id)
            return redirect(preview_url)
        else:
            return render(request, "wiki_form.html", {"form": form})



def wiki(request,project_id):
    """wiki首页"""
    wiki_id = request.GET.get("wiki_id")

    if wiki_id:
        if not wiki_id.isdigit():
            return render(request, "wiki.html")
        wiki_object = Wiki.objects.filter(id=wiki_id,project_id=project_id).first()
        return render(request, "wiki.html",{"wiki_object":wiki_object})
    else:
        return render(request, "wiki.html")


def wiki_catalog(request,project_id):

    wikiitems = Wiki.objects.filter(project_id=project_id).values().order_by("depth","id")


    return JsonResponse({"status":True,"data":list(wikiitems)})


class Wiki_add(View):
    def get(self,request,project_id):
        form =WikiModelForm(request)
        return render(request, "wiki_form.html", {"form":form})


    def post(self,request,project_id):

        form = WikiModelForm(request,data=request.POST)
        if form.is_valid():
            if form.instance.parent:
                form.instance.depth = form.instance.parent.depth+1 #二级标签是父类的深度+自己的深度等于第三个深度
            else:
                form.instance.depth = 1
            form.instance.project = request.tracer.project
            form.save()
            url = reverse("project:wiki",kwargs={"project_id":project_id})
            return redirect(url)
        return render(request, "wiki_form.html", {"form": form, "error":form.errors})

@csrf_exempt
def wiki_upload(request,project_id):
    #插件上传图片

    image_obj = request.FILES.get("editormd-image-file")
    ext = image_obj.name.rsplit(".")[-1]
    key = "{}.{}".format(uid(request.tracer.user.mobile_phone),ext)

    image_url = upload_file(request.tracer.project.bucket,image_obj,key)
    print(image_url)

    result = {
        "success":1,
        "message":None,
        "url":image_url
    }
    return JsonResponse(result)

