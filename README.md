# FLASK-MQTT Serv
## 概述
- 用于个人服务型工具，没有UI界面只是服务
## FLASK
- FLASK是基础服务，必须不可关闭。
## MQTT
- 通过配置文件可设置是否启用MQTT模式、
## 配置文件
- config/config.json内标注了详细的解释，详情看配置文件
- 注意修改**APP_NAME**(这关系到安装服务时候显示的名称)
- 注意修改**FLASK**部分的,HOST,PORT
- 注意修改**MQTT**部分的,HOST,PORT
# 运行与安装
## 调试入口
- 运行main.py是入口调试是可直接启动main.py文件进行调试
## 准备条件
- [python-3.8.10](https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe)
## 运行
- 使用管理员权限运行cmd.exe
- 进入Serv根目录
- 输入命令：
``` cmd
 x:\> run 或 run.bat
```
- 运行后窗口隐藏的可通过任务管理器进行杀死进程关闭服务
- 进程名是[APP_NAME], [APP_NAME]来自于config/config.json内的配置项，可以随时更改。

## 开机启动
- win+r键 复制下面路径 并打开
```
%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```
- 把serv路径下的run.bat创建快捷方式，放在上述打开路路径里面即可。
## 初次运行 run
- 为了不影响本机实体环境，当第一次运行run时 会在serv目录下自动创建_venv虚拟环境文件夹，该文件夹是虚拟环境
- 第一次run时在安装完包后会出现一个异常，程序自动重启因为这个包安装完需要重启一下忽略即可。
- 除第一次以外的无法启动都是有问题的。请查看命令窗口 查看方法 run.bat 编辑 将 -WindowStyle Hidden 删除即可




