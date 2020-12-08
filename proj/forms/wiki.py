#coding:utf-8


from django import forms
from proj.models import Wiki
from forms.base_bootstrap import Base_Bootstrap

class WikiModelForm(Base_Bootstrap,forms.ModelForm):

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request= request
        total_data_list = [("","请选择"),]
        data_list = Wiki.objects.filter(project=self.request.tracer.project).values_list("id","title")
        total_data_list.extend(data_list)
        self.fields["parent"].choices = total_data_list #显示父级文章选项和请选择标签

    class Meta:
        model = Wiki
        exclude = ["project","depth",]#过滤叼project 和 depth

