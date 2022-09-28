"""
    全局管理
"""
class GlobalManager(object):

    def __init__(self, app=None):
        """
            初始化
        """
        self.app = app
        self._manager = {}

        if self.app is not None:
            self.__init__(self, app)

    def init_app(self, app):
        """
            注册
            app = Flask(__name__)
            在下注册
            GlobalManager().init_app(app)
        """
        if not hasattr(app, 'GlobalManager'):
            app.GlobalManager = self
        self.app = app

    def get(self, key):
        """
            根据key获取值
        return: dict
        """
        return self._manager.get(key, None)

    def set(self, key, value):
        """
            设置 属性 键,值
        param: <key> 字典 键
        param: <value> 字典 值
        """
        self._manager.update({key: value})

    def remove(self, key, value=None):
        # FIXME:不能使用，功能没有写完
        """
            删除
        param: <key> 字典 键
        param: <key> 字典 值
        """
        if value is None:
            self._manager.pop(key)
        else:
            self._manager.get(key).pop(value)