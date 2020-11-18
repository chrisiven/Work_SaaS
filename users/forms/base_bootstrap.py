#coding:utf-8
from django import forms


class Base_Bootstrap(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = "请输入{}".format(field.label)
            # field.widget.attrs["value"] = "test"