import os

def search_config_file_path():
    '''
    查找所有以config命名的.json的文件
    如：config.json    
    '''
    config_file_paths = []
    root_path = os.getcwd()
    for root, dirs, files in os.walk(root_path, topdown=False):
        for filename in files:
            if 'config.json' in filename:
                print('discovery profile -> %s ' % filename)
                print('%s' % os.path.join(root, filename))
                print()
                config_file_paths.append(os.path.join(root, filename))
    return config_file_paths
