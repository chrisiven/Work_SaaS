from django.db import models

# Create your models here.
from proj.models import Project,PricePolicy

class UserInfo(models.Model):

    username = models.CharField(verbose_name="用户名",max_length=32)
    email = models.CharField(verbose_name="邮箱",max_length=32,unique=True)
    mobile_phone = models.CharField(verbose_name="手机号",max_length=11,unique=True)
    password = models.CharField(verbose_name="密码",max_length=100)
    price_policy = models.ForeignKey("proj.PricePolicy",on_delete=models.CASCADE,default=1)
    project_num = models.SmallIntegerField(verbose_name="项目个数",default=0)

    class Meta:
        db_table = "userprofile"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
