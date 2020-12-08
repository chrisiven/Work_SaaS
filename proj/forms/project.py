#coding:utf-8

from forms.base_bootstrap import Base_Bootstrap
from proj import models
from django import forms
from django.core.validators import ValidationError
from forms.widgets import ColorRadioSelect

class ProjectModelForm(Base_Bootstrap,forms.ModelForm):
    # desc = forms.CharField(widget=forms.Textarea())
    bootstrap_classs_exclude = ["color"]
    class Meta:
        model = models.Project
        fields = ["name","color","desc"]
        widgets = {
            "desc":forms.Textarea(),
            "color":ColorRadioSelect(attrs={"class":"color-radio"})

        }

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request
    def clean_name(self):
        name = self.cleaned_data.get("name")
        exists = models.Project.objects.filter(name=name,creator=self.request.tracer.user).exists()


        """
        1.判断当前项目名称是否存在
        2.判断当前用户权限是否已经无法创建新的项目了
        3.判断该用户
        """
        if exists:
            raise ValidationError("该项目已存在")
        count = models.Project.objects.filter(creator=self.request.tracer.user).count()
        if count >= self.request.tracer.price_policy.project_num:
            raise ValidationError("项目个数超限,请购买套餐")
        return name
