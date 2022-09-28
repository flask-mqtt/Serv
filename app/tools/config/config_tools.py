import sys
from app.tools.file_operations.get_file_path import get_file_path
from app.tools.file_operations.read_json_file import read_json_file

def init_config():
    """
        初始化 配置文件
    """
    configs = {}
    try:
        config_file_paths = get_file_path('config.json')
        for config_file_path in config_file_paths:
            data = read_json_file(config_file_path)
            if len(data) > 0:
                configs.update(data)
        return configs
    except Exception as ex:
        print(ex)
        sys.exit()