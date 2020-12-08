## day 09

### wiki后续开发
- wiki删除
- wiki编程
- markdown编辑器
- - 添加，编辑
- - 预览页面
- markdown上传图片的功能

### 今日详细

- wiki删除
    思路就是获取当前wiki文章的id然后进入到后台删除
    遇到问题了:就是发送请求的时候，有时候无法获取del_id! 
    解决方案:django的url可以直接传递参数在<a>里面，传递到后台进行删除
    
    优化方案:在删除的过程中 可以弹出个确认框
    
- wiki编辑
    和我想的完全一样 都是在add的页面简单编辑

#### markdown安装以及使用
-    1.txtarea框通过div包裹以便以后查找并转化为编辑器

-    2.应用js和css
```djangotemplate
    {% load static %}
        <script src="{% static 'plugin/editor.md/editormd.min.js' %}"></script>
        <link rel="stylesheet" href="{% static 'plugin/editor.md/css/editormd.min.css' %}">

```
    
-   3.初始化
```javascript
    var editor = editormd("editor",{
            width:"100%",
            height:"100%",
            path:"{% static 'plugin/editor.md/lib/' %}"
        })
```
         

-   4.全屏样式
````javascript
    .editormd-fullscreen{
            z-index:1001;
        }
    
````
        
- 将textarea变为editor

#### markdown展示效果
- 1.textarea框通过div包裹以后方便查找和转化为编辑器
````html
    <div id="xxx">...</div>
````
- 2.应用js和css
```djangotemplate
    <link rel="stylesheet" href="{% static 'plugin/editor.md/css/editormd.preview.min.css' %}">
    

    <script src="{% static 'plugin/editor.md/editormd.min.js' %}"></script>
    <script src="{% static 'plugin/editor.md/lib/flowchart.min.js' %}"></script>
    <script src="{% static 'plugin/editor.md/lib/prettify.min.js' %}"></script>
    <script src="{% static 'plugin/editor.md/lib/raphael.min.js' %}"></script>
    <script src="{% static 'plugin/editor.md/lib/underscore.min.js' %}"></script>
    <script src="{% static 'plugin/editor.md/lib/sequence-diagram.min.js' %}"></script>
    <script src="{% static 'plugin/editor.md/lib/marked.min.js' %}"></script>
    <script src="{% static 'plugin/editor.md/lib/jquery.flowchart.min.js' %}"></script>
```
-   3.初始化
```javascript
    function initPreviewMarkDown(){
                editormd.markdownToHTML("previewMarkdown",
                    {
                        htmlDecode:"style,script,iframe"
                    })
        }

```

## 项目中集成COS
    希望我们的项目用到的图片可以放在cos中,防止我们的服务器处理图片压力过大，分摊压力
- 编写上传文件的脚本
- markdown上传图片到cos!




## 总结
    1.明白一个新的概念，你可以争取自己写一些轮子，保证以后的开发使用。 不断地写轮子积累经验
    然后就可以成为老的程序员了
    
    完成:编辑器实现markdown编辑和预览
    欠缺:通过markdown组件上传图片