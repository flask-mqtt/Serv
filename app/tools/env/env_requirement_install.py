import re
import sys
import subprocess as sp

def requirement_install(requirements):
    
    """
        使用 pip 检测 requirements.json 中规定的包
    """
    requirements = requirements
    packages = sp.getoutput('pip3 list')
    if packages.find('python.exe -m pip install --upgrade pip') > -1:
        varsion_temp = packages.split('pip version')[1].split('is available')[0].split(' ')
        current_varsion = varsion_temp[1][:len(varsion_temp)]
        new_varsion = varsion_temp[4]
        print('\033[0;33;2m正在将pip %s 版本升级到 -> %s ...\033[0m' % (current_varsion,new_varsion))
        res = sp.getoutput('python.exe -m pip install --upgrade pip')
        if res.find('Could not find an activated virtualenv (required)') > -1:
            res = '检测到 pip 安装被锁定虚拟环境virtualenv锁定 任何扩展包只能在virtualenv虚拟环境中安装。如果需要安装请先激活对应的虚拟环境。'
            print('\033[0;31;2m%s\033[0m' % res)
            sys.exit()
        print('\033[0;33;2m %s \033[0m' % res)
    packages = packages.replace('Package', '').replace(
        'Version', '').replace(' \n ', '')
    packages = re.sub('\\n-+', ' ', packages)
    packages = re.sub('-+\\n', ' ', packages)
    packages = re.sub(' +', ' ', packages)
    packages = re.sub('^ ', '', packages)
    package_list = packages.split('\n')

    print('\033[0;32;2mpip %s\033[0m' % sp.getoutput('pip3 -V').split(' ')[1])
    for requirement in requirements['requirements']:
        existPackage = False
        for item in package_list:
            name = item.split(' ')[0]
            version = item.split(' ')[1]
            if name.upper() == requirement["name"].upper():
                existPackage = True
                print('\033[0;32;2m%s %s\033[0m' % (name, version))
                break
        if not existPackage:
            install_package(requirement["name"], requirement["version"])


def install_package(package_name, version):
    """
        使用 pip 安装 python 包
    param: <package_name> 包名
    param: <version> 版本
    return:
    """
    if not package_name:
        return
    try:
        error = None
        print('\033[0;33;2m正在安装 %s ...\033[0m' % package_name)
        if version and version != '' and version != 'release':
            os_result = sp.getoutput('pip3 install %s==%s' %
                                     (package_name, version))
        else:
            os_result = sp.getoutput('pip3 install %s' % package_name)
            if os_result.find('ERROR:') > -1:
                error = True

                if os_result.find('Could not find an activated virtualenv (required)') > -1:
                    os_result = '检测到 pip 安装被锁定虚拟环境virtualenv锁定 任何扩展包只能在virtualenv虚拟环境中安装。如果需要安装请先激活对应的虚拟环境。'
                    print('\033[0;31;2m%s\033[0m' % os_result)
                    sys.exit()
                    
                print('\033[0;31;2m%s\033[0m' % os_result)

        if not error:
            os_result = sp.getoutput('pip3 show --files %s' % package_name)
            if len(os_result.split('\n')[1].split(': ')[1]) > -1:
                print('\033[0;32;2m%s Version: %s 安装完成\033[0m' % (
                    package_name, os_result.split('\n')[1].split(': ')[1]))

    except Exception as ex:
        print(ex)

