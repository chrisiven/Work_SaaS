
## 今日概要
    
    1.通过email来发送信息
    2.Django得modelForm组件
    3.redis (内存型数据库)
    
    
    
    
    注册逻辑设计讨论  ==> 开发 
    
    
    
    昨日内容回顾
        local_settings的作用?
            local_settings是django开发者/测试者的自己在项目中的配置. 防止泄露自己的数据信息.
        .gitignore是干啥的? 
            将不需要的文件写进到这个文件内,然后git在提交的时候就会忽略掉里面匹配的出的文件
        虚拟环境的作用?
            将开发环境和线上环境和测试环境区别开来,避免因为环境混杂导致项目出错.
            
## django的modelform


点击获取验证码；
    1.获取手机号码
    2.点击获取验证码
    3.验证码处理时效是60s
    