import sys
from app.tools.file_operations.get_file_path import get_file_path
from app.tools.file_operations.read_json_file import read_json_file
from app.tools.env.env_requirement_install import requirement_install


def init_env():
    """
        初始化 配置文件
    """
    tmp = []
    requirements = {}
    try:
        requirements_file_paths = get_file_path('requirements.json')
        for requirements_file_path in requirements_file_paths:
            data = read_json_file(requirements_file_path)
            if len(data['requirements']) > 0:
                for item in data['requirements']:
                    tmp.append(item)
        requirements.update({"requirements": tmp})
        requirement_install(requirements)
    except Exception as ex:
        print(ex)
        sys.exit()
