from werkzeug.utils import find_modules, import_string
# import importlib

def register_blueprints(flask_app=None, project_name=None, key_attribute='api'):
    """
        自动注册Flask蓝图 
    param: <key_attribute> 蓝图文件的str关键字
    param: <project_name> 用于查找子模块的包名称。
    param: <flask_app> flask 实例
    return:
    """
    if not flask_app:
        return None
    if project_name:
        modules = find_modules(
            f'{project_name}', include_packages=True, recursive=True)
        for name in modules:
            module = import_string(name)
            # module_i = importlib.import_module(name)
            if hasattr(module, key_attribute):
                flask_app.register_blueprint(getattr(module, key_attribute))
