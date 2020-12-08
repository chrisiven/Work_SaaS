day01 前戏



## 今日概要

        虚拟环境

        项目架构:local_settings

        git应用实战 (代码每天提交)



## 今日详细

    1.虚拟环境  virtualenv 
    
        安装
            pip install virtualenv 		
                
        创建虚拟环境
            virtualenv 环境名称  
            #注意 ： 创建 [环境名称] 文件夹 ， 放置所有的环境  进入指定目录 D:/envs
    

        环境名称:
            virtualenv 环境名称 --python==python2.x/3.x

    2.激活/退出虚拟环境
        激活:
            windows :
                workon [环境名称]
            mac:
                source [路径][环境名称]
        退出:
            windows:
                deactivate #直接 deactivate
            mac:
                deactivate
                
    3.安装/卸载 模块
        
        安装:
            pip install [模块名称]
        卸载：
            pip uninstall [模块名称]
           
    
    
    4. 本地配置 local_settings.py
        每个人保留自己的文件内容



    5.本地推送git:
        详细:
            git init 初始化
            git add . # .代表所有的文件 
            git commit -m "just test commit" 
            
            #提交到远程仓库
            
            # 1.添加远程仓库        
            git remote add origin  https://github.com/chrisiven/Work_SaaS.git
            
            # 提交到远程仓库
            git push origin maste r
     
     
    作业:
        虚拟环境:tracer
        创建django项目：tracer
        git仓库:tracer (.gitignore)
        写文档:
            思考:程序员如何写好一个文档? 既美观,意图又强!