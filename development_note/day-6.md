## 今日概要

1.展示项目
2.星标项目
3.添加项目:颜色选择
4.项目切换:项目菜单处置



## 今日详细：
    

    #1 从数据库中获取两部分的数据
        # 我创建的所有项目, 已星标 未星标
        # 我参与的所有项目  已星标 未星标 

    #2.提取已星标
       # 列表 = 循环 [我创建的所有项目] + [我参与的所有项目] 把已星标的数据提取
    #然后就得到三个列表


### 1.星标项目
    展示星标
        project/add_star/
    取消星标
        project/cancel_star/



### 2.1 部分样式应用bootstrap
    

```python
in base_Bootstrap.py
class Base_Bootstrap:
    bootstrap_classs_exclude = []
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            if name in self.bootstrap_classs_exclude:
                continue
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = "请输入{}".format(field.label)
            # field.widget.attrs["value"] = "test"


```

```python

in forms.project.py

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

```

### 2.2 定制ModelForm的插件
```python
in project.forms.project.py

    class Meta:
        model = models.Project
        fields = ["name","color","desc"]
        widgets = {
            "desc":forms.Textarea(),
            "color":ColorRadioSelect(attrs={"class":"color-radio"})

        }
```

```python
in forms.widgets.py

class ColorRadioSelect(RadioSelect):
    template_name = 'widgets/color_radio/radio.html'
    option_template_name = 'widgets/color_radio/radio_option.html'
```

### 2.3 切换菜单
    1.数据库中获取
        我创建,参与的
    2.循环展示
    
    3.当前页面需要显示 / 其他页面也需要显示[inclusion_tag]
    
```python
from django.template import Library 
from proj import models
register = Library()
@register.inclusion_tag("inclusion/all_projec_list.html")
def all_project_list(request):
    my_creater_project = models.Project.objects.filter(creator=request.tracer.user)
    my_join_project = models.ProjectUser.objects.filter(user=request.tracer.user)

    return {"my_project":my_creater_project,"join_project":my_join_project}
# 就是将一个特定的功能放入到一个公共模块中去,省的一个个调用麻烦.
#步骤就是:
    1.在app下创建一个文件夹,里面放一个.py的文件
    2.调用from django.template import Library的inclusion_tag将你的模块html进行注册
    3.然后在你的.py文件内写入你所要被调用的信息，比如查询的信息
    4.通过封装字典进行返回
    5.如果需要request的参与就在前端的参数上写入request
```


## 总结
#### 1.项目实现思路
#### 2.星标/取消星标
#### 3.inclusion_tag 实现目标切换
#### 4.项目菜单

- 中间件 process_view  
- inclusion_tag
- 路由分发
- - include("xxx.url")
- - include([asdasdas,asdasd,asdasd]

#### 5.颜色选则：源码+扩展[实现]        




# 面试了解学习
- request的生命周期
- request请求所经过了哪些组件?
- 中间件的处理顺序是?
