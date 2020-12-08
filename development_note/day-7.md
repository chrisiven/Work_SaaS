## day-7 聊聊wiki
### 聊聊开发文档~ 
    就是这个项目所要实现的是什么东西  所要求的技术是什么水准的~ 本项目的wiki就是如此类型的~
    

## 今日概要

-  表结构设计
-  快速开发
-  应用markdown组件
-  基于腾讯cos做上传



### 今日详细
#### 表结构设计
    wiki表:
        标题 内容 项目标记(id)
        id title content project_id
```python
from django.db import models
class Wiki(models.Model):

    project = models.ForeignKey("Project",on_delete=models.CASCADE)
    title = models.CharField(verbose_name="标题",max_length=32)
    content = models.TextField(verbose_name="内容")
    parent = models.ForeignKey(verbose_name="父文章",to="self",on_delete=models.CASCADE,null=True,blank=True,related_name="children")
    

```
#### wiki首页展示

    1.首页文章展示
        首页:已完成
        多级目录:     
    2.添加文章
    3.预览文章
    4.修改文章
    5.删除文章












### 今日思考
    django的关联字段 : 什么是正关联? 什么是反关联?
```python
from django.db import models

class level(models.Model):

    l_name = models.CharField(max_length=50,verbose_name="等级名称")
    
    def __str__(self):
        return self.l_name
  
  
class userinfo(models.Model):

    u_name = models.CharField(max_length=50,verbose_name="用户名称")
    u_level = models.ForeignKey(level,related_name="lev")
  
    def __str__(self):
        return self.u_name


# 正向查询
userinfo.object.get(pk=1).u_level

# 反向查询
level.object.get(pk=1).lev.l_name


```
    
### 面试工作必备
- 需求分析能力,要分析项目有哪些需求,看需求来设计表结构
