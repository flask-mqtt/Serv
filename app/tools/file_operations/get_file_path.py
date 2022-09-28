import os

def get_file_path(file):
    config_file_paths = []
    root_path = os.getcwd()
    for root, dirs, files in os.walk(root_path, topdown=False):
        for filename in files:
            if file in filename:
                print('discovery profile -> %s ' % filename)
                print('%s' % os.path.join(root, filename))
                print()
                config_file_paths.append(os.path.join(root, filename))
    return config_file_paths
