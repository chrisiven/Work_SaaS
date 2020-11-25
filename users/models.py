from django.db import models

# Create your models here.
from proj.models import PricePolicy

class UserInfo(models.Model):

    username = models.CharField(verbose_name="用户名",max_length=32)
    email = models.CharField(verbose_name="邮箱",max_length=32,unique=True)
    mobile_phone = models.CharField(verbose_name="手机号",max_length=11,unique=True)
    password = models.CharField(verbose_name="密码",max_length=100)
    # price_policy = models.ForeignKey(verbose_name="价格策略","")

    class Meta:
        db_table = "userprofile"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
