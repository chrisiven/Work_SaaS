from django.db import models

# Create your models here.
import users


class PricePolicy(models.Model):# this is Teacher·wu create table
    category_choices = (
        (1,"免费版"),
        (2,"收费版"),
        (3,"其他")
    )
    category = models.SmallIntegerField(verbose_name="收费类型",default=1,choices=category_choices) #一开始应该是免费版
    title = models.CharField(verbose_name="标题",max_length=32)
    price = models.PositiveIntegerField(verbose_name="价格")
    project_num = models.PositiveIntegerField(verbose_name="项目数")
    project_member = models.PositiveIntegerField(verbose_name="项目成员数")
    project_space =models.PositiveIntegerField(verbose_name="单项目空间")
    pro_file_size =models.PositiveIntegerField(verbose_name="单文件大小")
    create_datetime = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)

    class Meta:
        db_table = "pricepolicy"
        verbose_name = "价格表"
        verbose_name_plural = verbose_name
class  Transaction(models.Model):#交易记录表
    status_code = (
        (0,"未支付"),
        (1,"已支付"),
    )
    status = models.SmallIntegerField(verbose_name="交易状态",choices=status_code)
    order_id = models.CharField(verbose_name="订单号",max_length=20,unique=True)
    user= models.ForeignKey("users.UserInfo",on_delete=models.CASCADE)
    price_policy = models.ForeignKey("PricePolicy",on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name="数量/年",help_text="0表示无限期")
    price = models.IntegerField(verbose_name="实际支付价格")
    start_datetime = models.DateTimeField(verbose_name="服务开始时间",null=True,blank=True)
    end_datetime = models.DateTimeField(verbose_name="服务结束时间",null=True,blank=True)
    create_datetime = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)

    class Meta:
        db_table = "transaction"
        verbose_name = "交易表"
        verbose_name_plural = verbose_name


class Project(models.Model):
    COLOR_CHOICES = (
        (1,"#56b8eb"),
        (2,"#f28033"),
        (3,"#ebc656"),
        (4,"#a2d148"),
        (5,"#208fa4"),
        (6,"#7461c2"),
        (7,"#20bfa3")
    )
    name = models.CharField(verbose_name="项目名称",max_length=32)
    color = models.SmallIntegerField(verbose_name="项目颜色",choices=COLOR_CHOICES,default=1)
    desc = models.CharField(verbose_name="项目描述",max_length=255,null=True,blank=True)
    user_space = models.IntegerField(verbose_name="项目已使用空间",default=0)
    star = models.BooleanField(verbose_name="星标",default=False)
    join_count = models.SmallIntegerField(verbose_name="参与人数",default=1)
    creator = models.ForeignKey("users.UserInfo",on_delete=models.CASCADE,verbose_name="创建者")
    create_datetime = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)

    class Meta:
        db_table = "project"
        verbose_name = "项目表"
        verbose_name_plural = verbose_name

class ProjectUser(models.Model):
    user = models.ForeignKey("users.UserInfo",on_delete=models.CASCADE)
    project = models.ForeignKey("Project",on_delete=models.CASCADE)
    star = models.BooleanField(default=False,verbose_name="星标")
    create_datetime = models.DateTimeField(verbose_name="加入时间",auto_now_add = True)

    class Meta:
        db_table = "projectuser"
        verbose_name = "项目参与者表"
        verbose_name_plural = verbose_name


# class PriceStrategy(models.Model): #this my create table
#
#     id = models.AutoField(primary_key = True,unique=True,verbose_name="策略id")
#     category = models.CharField(max_length=10,verbose_name="价格分类")
#     title = models.CharField(max_length=10,verbose_name="价格标题")
#     price = models.IntegerField(verbose_name="价格")
#     project_members = models.IntegerField(verbose_name="项目成员")
#     project_space = models.IntegerField(verbose_name="项目空间")
#     file_space = models.IntegerField(verbose_name="单个文件的空间")
#     #价格表不需要关联用户
#     class Meta:
#         db_table = "pricestrategy"
#         verbose_name = "价格策略表"
#         verbose_name_plural = verbose_name
#         ordering = ["project_members","project_space"]



# class Transaction(models.Model): #this my create table
#
#     # 交易表需要关联用户以及价格策略表
#     id = models.AutoField(primary_key=True,unique=True,verbose_name="交易id")
#     order_id = models.IntegerField(verbose_name="订单id",unique=True) #unique
#     state = models.CharField(max_length=20,verbose_name="交易状态")
#     user = models.ForeignKey("users.UserInfo",on_delete=models.CASCADE)
#     price_category = models.ForeignKey("PriceStrategy",on_delete=models.CASCADE)
#     actual_delivery = models.IntegerField(verbose_name="实际支付")
#     service_start_time = models.DateField(auto_now_add=True,verbose_name="服务开启时间")
#     service_end_time = models.DateField(verbose_name="服务结束时间") #得自行编写!
#     number = models.IntegerField(verbose_name="购买数量/年")
#
#     class Meta:
#         db_table = "transaction"
#         verbose_name = "交易表"
#         verbose_name_plural = verbose_name
#         ordering = ["number","id","order_id","actual_delivery"]
