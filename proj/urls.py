"""SaaS_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,include

from .views import project,proj_manage,wiki
app_name = "project"
urlpatterns = [
    # 项目列表
    path("list/", project.ProjectView.as_view(), name="project_list"),
    path("add_star/",project.addStar,name="addstar"),
    path("cancel_star/",project.cancelStar,name="cancelStar"),

    # 项目管理 完成项目才是关键
    path("manage/<project_id>/dashboard/", proj_manage.dashboard, name="dashboard"),
    path("manage/<project_id>/issues/", proj_manage.issues, name="issues"),
    path("manage/<project_id>/statistics/", proj_manage.statistics, name="statistics"),
    path("manage/<project_id>/file/", proj_manage.file, name="file"),

    path("manage/<project_id>/wiki/", wiki.wiki, name="wiki"),
    path("manage/<project_id>/wiki/upload/", wiki.wiki_upload, name="wiki_upload"),
    path("manage/<project_id>/wiki/add/",wiki.Wiki_add.as_view(),name="wiki_add"),
    path("manage/<project_id>/wiki/catalog/",wiki.wiki_catalog,name="wiki_catalog"),
    path("manage/<project_id>/wiki/delete/<del_id>",wiki.wiki_delete,name="wiki_delete"),
    path("manage/<project_id>/wiki/edit/<wiki_id>",wiki.EditWiki.as_view(),name="edit_wiki"),

    path("manage/<project_id>/setting/", proj_manage.setting, name="setting"),

]
