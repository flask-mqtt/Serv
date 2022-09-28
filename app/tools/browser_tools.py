from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from msedge.selenium_tools import Edge, EdgeOptions
from app.tools.my_global import *
import time
import os


SAVE_SCREENSHOT_PATH = 'Debug/Screenshots/%s/' % time.strftime(
    '%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
SAVE_SCREENSHOT_FILENAME = 'screenshot.jpg'

PAGE_ROURCE_PATH = 'Debug/Rources/%s/' % time.strftime(
    '%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
PAGE_ROURCE_FILENAME = 'result.html'


class BrowserTools:
    driver = None

    def __init__(self):
        app_config = get_global_manager('config', 'CONFIG')
        public_config = app_config['BROWSER']['PUBLIC']
        edge_chrome_config = app_config['BROWSER']['EDGE_CHROME']

        # 初始化相关目录
        if not os.path.exists(public_config.get('DOWNLOAD_DIRECTORY')):
            os.makedirs(public_config.get('DOWNLOAD_DIRECTORY'))

        # region 规避检测
        '''
            ## stealth.min.js
            - part.1 安装 node.js 
            - part.2 确认可以运行 npm 命令
            - part.3 使用cmd 或 powershell 进入 项目的drivers目录 如 cd d:\Trinity\drivers
            - part.4 运行命令 
            ```
                npx extract-stealth-evasions
            ```
            - 并等待下载完成 文件大小 150mb 左右 （挂梯子速度快 如果慢自己百度npm源更换）
            - 下载完成后得到 stealth.min.js 不能删除 项目要用
        '''
        with open('drivers/stealth.min.js') as f:
            js = f.read()
        # endregion
        
        if public_config.get('DRIVER').lower() == 'edge':
            try:
                options = EdgeOptions()
                options.use_chromium = True
                prefs = {}
                if edge_chrome_config.get('HEADLESS'):
                    # region 规避检测
                    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
                    # options.add_experimental_option('useAutomationExtension', False)
                    prefs.update({'profile.default_content_settings.popups': 0,
                            #  'download.default_directory': edge_chrome_config.get('DOWNLOAD_DIRECTORY'),
                             # 关闭DevTools listening on ws://127.0.0.1的打印
                             'excludeSwitches': ['enable-logging']
                             })
                    options.add_argument(
                        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
                    # endregion

                    options.add_argument("headless")

                    # 专门应对无头浏览器中不能最大化屏幕的方案
                    options.add_argument("--window-size=1920,1080")

                if edge_chrome_config.get('DISABLE_GPU'):
                    options.add_argument("disable-gpu")

                if edge_chrome_config.get('NO_SANDBOX'):
                    options.add_argument("no-sandbox")

                if edge_chrome_config.get('DISABLE_SETUID_SANDBOX'):
                    options.add_argument("disable-setuid-sandbox")

                if edge_chrome_config.get('DISABLE_DEV_SHM_USAGE'):
                    options.add_argument("disable-dev-shm-usage")

                # INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
                options.add_argument('log-level=%s' %
                                     edge_chrome_config.get('LOG_LEVEL'))

                # 对应Passthrough is not supported, GL is disabled 错误
                options.add_argument("--disable-software-rasterizer")
                options.add_argument("-enable-webgl --no-sandbox --disable-dev-shm-usage")
                
                
                options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

                # 配置下载路径
                prefs.update({'download.default_directory': os.path.join(
                    os.getcwd(), public_config.get('DOWNLOAD_DIRECTORY'))})
                
                # 禁止加载图像
                if edge_chrome_config.get('MANAGED_DEFAULT_CONTENT_SETTINGS_IMAGES') == 2:
                    prefs.update({'profile.managed_default_content_settings.images': 2})


                options.add_experimental_option("prefs", prefs)

                drivers_path = os.path.join(
                    os.getcwd(), 'drivers', 'msedgedriver.exe')

                self.driver = Edge(
                    options=options, executable_path=drivers_path)

                # region 规避检测 位置不能换 必须在 self.driver = Edge(options=options) 下面
                self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": js
                })
                # endregion
            except Exception as ex:
                print(ex)
                print(
                    'Edge 浏览器驱动异常 请尝试修复驱动\n驱动下载:https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/')
                print('注意浏览器与驱动版本大号需要一致')
                print('下载后将文件放在项目的drivers目录下')

        elif public_config.get('DRIVER').lower().lower() == 'chrome':
            try:
                self.driver = webdriver.Chrome()
                options = webdriver.ChromeOptions()
                if edge_chrome_config.get('HEADLESS'):
                    options.add_argument("--headless")
                if edge_chrome_config.get('DISABLE_GPU'):
                    options.add_argument("--disable-gpu")
                if edge_chrome_config.get('NO_SANDBOX'):
                    options.add_argument("--no-sandbox")
                if edge_chrome_config.get('DISABLE_SETUID_SANDBOX'):
                    options.add_argument("--disable-setuid-sandbox")
                if edge_chrome_config.get('DISABLE_DEV_SHM_USAGE'):
                    options.add_argument("--disable-dev-shm-usage")

                # INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
                options.add_argument('log-level=%s' %
                                     edge_chrome_config.get('LOG_LEVEL'))

                self.driver = webdriver.Chrome(options=options)
            except Exception as ex:
                print(ex)
                print(
                    'Chrome 浏览器驱动异常 请尝试修复驱动\n驱动下载:https://chromedriver.storage.googleapis.com/index.html')
                print('注意浏览器与驱动版本大号需要一致')
                print('下载后将文件名修改为 chromedriver.exe')
                print('将 chromedriver.exe 复制到 Python安装目录下')

        elif public_config.get('DRIVER').lower().lower() == 'firefox':
            try:
                pass
                # from selenium.webdriver.firefox.options import Options
                # self.driver = webdriver.Firefox()
                # options = Options()
                # if app_config.get('HEADLESS'):
                #     options.add_argument("headless")
                # if app_config.get('DISABLE_GPU'):
                #     options.add_argument("disable-gpu")
                # if app_config.get('NO_SANDBOX'):
                #     options.add_argument("no-sandbox")
                # if app_config.get('DISABLE_SETUID_SANDBOX'):
                #     options.add_argument("disable-setuid-sandbox")
                # if app_config.get('DISABLE_DEV_SHM_USAGE'):
                #     options.add_argument("disable-dev-shm-usage")

                # # INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
                # options.add_argument('log-level=%s' %
                #                      app_config.get('LOG_LEVEL'))

                # self.driver = webdriver.Firefox(options=options)
            except Exception as ex:
                print(ex)
                print(
                    'Firefox 浏览器驱动异常 请尝试修复驱动\n驱动下载:https://github.com/mozilla/geckodriver/releases')
                print('注意浏览器与驱动版本大号需要一致')
                print('下载后将文件名修改为 geckodriver.exe')
                print('将 geckodriver.exe 复制到 Python安装目录下')
        else:
            print('没有找到任何模拟浏览器驱动\n请在程序的config/config.json配置文件中配置正确的模拟浏览器，只能是Edge,Chrome,Firefox其中之一\n并正确安装对应当前本地浏览器版本的驱动版本。\n')
            print(
                'Edge驱动下载地址:https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/')
            print('下载后将文件名修改为 MicrosoftWebDriver.exe\n')
            print('Chrome驱动下载地址:https://chromedriver.storage.googleapis.com/index.html')
            print('下载后将文件名修改为 chromedriver.exe\n')
            print('Firefox驱动下载地址:https://github.com/mozilla/geckodriver/releases')
            print('下载后将文件名修改为 geckodriver.exe\n')
            print(
                '将 MicrosoftWebDriver.exe chromedriver.exe geckodriver.exe 复制到 Python安装目录下')

        # return self.driver

    def request_test(self, url=None):
        '''
            测试被拦截的测试结果
        '''
        if url is None:
            self.driver.get('https://bot.sannysoft.com/')
        else:
            self.driver.get(url)

        self.save_page_source()

        self.screenshot()

    def save_page_source(self):
        # 保存源码
        if not os.path.exists(PAGE_ROURCE_PATH):
            os.makedirs(PAGE_ROURCE_PATH)

        source = self.driver.page_source
        try:
            with open(PAGE_ROURCE_PATH + PAGE_ROURCE_FILENAME, 'w', encoding='utf-8') as f:
                f.write(source)
        except Exception as ex:
            print(ex)

    def screenshot(self):
        '''
            截图
        '''
        if not os.path.exists(SAVE_SCREENSHOT_PATH):
            os.makedirs(SAVE_SCREENSHOT_PATH)
            name = SAVE_SCREENSHOT_FILENAME.split('.')[0]
            suffix = SAVE_SCREENSHOT_FILENAME.split('.')[1]
            filename = name + '_0.' + suffix
        else:
            temp_count = len(os.listdir(SAVE_SCREENSHOT_PATH))
            name = SAVE_SCREENSHOT_FILENAME.split('.')[0]
            suffix = SAVE_SCREENSHOT_FILENAME.split('.')[1]
            filename = name + '_' + str(temp_count) + '.' + suffix

        self.driver.save_screenshot(
            SAVE_SCREENSHOT_PATH + filename)

    def closeBrowser(self):
        self.driver.close()

    def scroll(self, webelement, x='0', y='-100'):
        '''
            控制滚动条到元素位置
            param: x 横向位置 default str '0'
            param: y 纵向位置 default str '-100'
        '''
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", webelement)
        self.driver.execute_script("window.scrollBy("+x+","+y+")")
