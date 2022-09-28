import json


def read_json_file(filepath):
    """
        读取json文件
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        app = f.read()
        f.close()
    return json.loads(app)
