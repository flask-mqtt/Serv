import os

def get_plugin_api_path(filepath,filename_):
    api_file_paths = []
    plugins_path = '%s%s%s' % (os.getcwd(),os.sep,os.sep.join(filepath.split('/')))
    for root, dirs, files in os.walk(plugins_path, topdown=False):
        for filename in files:
            if filename_ in filename:
                print('discovery profile -> %s ' % filename)
                print('%s' % os.path.join(root, filename))
                api_path = os.path.join(root, filename).replace(os.getcwd(),'').replace(filename,'').replace(os.sep,'.')
                api_path = api_path[1:len(api_path)-1]
                print('register_blueprints import path %s' % api_path)
                print()
                api_file_paths.append(api_path)
    return api_file_paths
