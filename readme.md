### 介绍

通过python脚本，一键获取Github host配置同时修改本地host文件，解决打不开Github的问题

也可以使用系统的自动任务让脚本定时运行，这样就避免了手动运行的麻烦


### 使用方式

本脚本是python脚本，需要先本地安装python3

脚本依赖了一个python第三方模块，安装好python后使用如下命令安装：`pip install requests`，该模块用于网络请求获取host配置

准备工作做好后，就可以直接双击脚本运行，或者在脚本所在目录，在控制台中使用命令运行脚本：

```bash
python ./githostool.py
```

运行时会请求管理员权限，因为host文件需要管理员权限才能进行修改

首次运行后会在脚本所在目录新建.log文件用于存放日志