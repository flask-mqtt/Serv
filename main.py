#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    作者:
        北京土著 2021-10-03
        30344386@qq.com
    平台:
        Windows Linux
"""

# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
# 用于环境检测与自动安装环境包 必须在这个位置不能改 内容不懂的也不能修改
# 否则程序将无法正常运行
# region 检测py版本
from distutils.util import execute
from email.policy import default
from os import execl, execlp
from app.tools.config.config_tools import init_config
import json
import sys
if sys.version_info < (3, 7, 9):
    print('请更新python版本 >= 3.7.9 (推荐使用 Python 3.7.9)')
    sys.exit()
# endregion


# region 检测node.js
# import subprocess as sp
# node = sp.getoutput('node --version')
# if node.find('\'node\'') > -1:
#     print('node.js正确安装，请确认已安装node.js并检查环境变量的配置是否正确。')
#     sys.exit()
# endregion

# region 安装环境包
CONFIG = init_config()

if CONFIG['AUTO_INSTALL_PACKAGES']:
    # 初始化自动安装 基本 环境支持包  ### 必须在这个位置不能改
    from app.tools.env.env_tools import init_env
    init_env()
# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

# region 包引用
from flask_mqtt import Mqtt
from flask_cors import *
from flask import Flask, request, jsonify
from app.tools.my_global import *
from app.tools.global_manager import GlobalManager
from app.tools.router_tools import register_blueprints
from app.tools.file_operations.get_api_path import get_plugin_api_path
# endregion

app = Flask(__name__)
GlobalManager().init_app(app)
CORS(app, supports_credentials=True)  # 允许跨域请求 为了配合vue 前端访问 flask

if CONFIG['MQTT']['ENABLE']:
    import requests
    app.config['MQTT_BROKER_URL'] = CONFIG['MQTT'][
        'MQTT_BROKER_URL']
    app.config['MQTT_BROKER_PORT'] = CONFIG['MQTT'][
        'MQTT_BROKER_PORT']
    app.config['MQTT_USERNAME'] = CONFIG['MQTT']['MQTT_USERNAME']
    app.config['MQTT_PASSWORD'] = CONFIG['MQTT']['MQTT_PASSWORD']
    app.config['MQTT_KEEPALIVE'] = CONFIG['MQTT'][
        'MQTT_KEEPALIVE']
    app.config['MQTT_TLS_ENABLED'] = CONFIG['MQTT'][
        'MQTT_TLS_ENABLED']
    MQTT_TOPIC = CONFIG['MQTT']['MQTT_TOPIC']
    # MQTT_TOPIC = '%s/' % (MQTT_TOPIC,CONFIG['APP_NAME'])
    TOPIC_SUB = '%s/%s/sub' % (MQTT_TOPIC,CONFIG['APP_NAME'])
    TOPIC_PUB = '%s/%s/pub' % (MQTT_TOPIC,CONFIG['APP_NAME'])
    try:
        mqtt = Mqtt(app)
    except Exception as ex:
        print(
            '\033[0;31;2m===============================================\033[0m'
        )
        print('\033[0;31;2mMQTT server connection failed\033[0m')
        print(
            '\033[0;31;2m===============================================\033[0m'
        )
        print('\033[0;33;2mIf you do not need the MQTT service function, please turn it off in config\033[0m')
        print('\033[0;33;2m------------------------------------------\033[0m')
        print('\033[0;33;2m...other config\033[0m')
        print('\033[0;33;2m"MQTT": {\033[0m')
        print('\033[0;33;2m     "ENABLE": False,\033[0m')
        print('\033[0;33;2m...other config\033[0m')
        print('\033[0;33;2m------------------------------------------\033[0m')
        print('\033[0;31;2mError: %s\033[0m' % ex)
        print(
            '\033[0;31;2mPlease check whether other parameters are correct\033[0m'
        )
        print(
            '\033[0;31;2msuch as (host, port, username, password......)\033[0m'
        )
        print(
            '\033[0;31;2m===============================================\033[0m'
        )
        sys.exit()

    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print(
                '\033[0;32;2m===============================================\033[0m'
            )
            print('\033[0;32;2mConnected successfully MQTT server\033[0m')
            print(
                '\033[0;32;2m===============================================\033[0m'
            )
            print('\033[0;33;2mserver: %s:%s\033[0m' %
                  (CONFIG['MQTT']['MQTT_BROKER_URL'],
                   CONFIG['MQTT']['MQTT_BROKER_PORT']))
                   
            print('\033[0;33;2mTOPIC: %s\033[0m' % MQTT_TOPIC)
            print('\033[0;33;2mTOPIC_SUB: %s\033[0m' % TOPIC_SUB)
            print('\033[0;33;2mTOPIC_PUB: %s\033[0m' % TOPIC_PUB)
            mqtt.subscribe(TOPIC_SUB)  # 订阅主题
            print(
                '\033[0;32;2m===============================================\033[0m'
            )
        else:
            print(
                '\033[0;31;2m===============================================\033[0m'
            )
            print('\033[0;31;2mMQTT server connection failed\033[0m')
            print('\033[0;31;2mBad connection. Code:\033[0m', rc)
            print(
                '\033[0;31;2mPlease check whether other parameters are correct\033[0m'
            )
            print(
                '\033[0;31;2msuch as (host, port, username, password......\033[0m)'
            )
            print(
                '\033[0;31;2m===============================================\033[0m'
            )

    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        data = dict(topic=message.topic, payload=message.payload.decode())
        topic = data.get('topic')
        try:
            msg = json.loads(data.get('payload')).get('msg')
            print('Received message on topic: %s with payload: %s' % (topic, msg))
        except Exception as ex:
            msg = data.get('payload')

        pub_msg = None
        if  type(msg) == dict:
            entrance = msg.get('entrance', None)
            manufacturer = msg.get('manufacturer', None)
            uid = msg.get('uid', None)
            value = msg.get('value', None)

            if value is not None:
                params = {
                    'manufacturer': manufacturer,
                    'uid': uid,
                    'value': value
                }
            else:
                params = {
                    'manufacturer': manufacturer,
                    'uid': uid
                }
            
            url= 'http://127.0.0.1:%s/%s' % (CONFIG['FLASK']['PORT'],entrance)
            result = requests.get(url=url, params=params)
            pub_msg = result.text
        else:
            pub_msg = msg
        url= 'http://127.0.0.1:%s/mqtt/pub' % CONFIG['FLASK']['PORT']
        params ={
            'msg': pub_msg
        }
        requests.get(url=url, params=params)
        
    '''
    MQTT 发布主题消息
    '''
    @app.route('/mqtt/pub', methods=["GET", "POST"])
    def publish_message():
        msg = request.args.get('msg', default=None)
        publish_result = mqtt.publish(TOPIC_PUB,msg)
        return jsonify({'code': publish_result[0]})

@app.before_first_request
def startup():
    set_global_manager('config', 'CONFIG', CONFIG)

# region 注册SERV蓝图
register_blueprints(app, 'app.core.api', 'api')


plugin_api_path = get_plugin_api_path('plugins','_api.py')
for item in plugin_api_path:
    register_blueprints(app, item, 'api')
# endregion

if __name__ == "__main__":
    try:
        app.run(
            threaded=True,  # 多线程
            host=CONFIG['FLASK']['HOST'],  # 地址
            port=CONFIG['FLASK']['PORT'],  # 端口
            debug=CONFIG['FLASK']['DEBUG'],  # 框架调试
            # 框架调试-自动重启
            use_reloader=CONFIG['FLASK']['DEBUG_RELOADER'])
    except Exception as ex:
        print(ex)
        input
        # 端口被占用杀死进程
        if 'WinError 10013' in str(ex):
            print('\033[0;36;2m [Error]:当前服务器端口 ' + CONFIG['PORT'] +
                  ' 被占用\033[0m')
