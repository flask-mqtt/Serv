
import io
import gzip
import requests
import cfscrape


class BasicRequests:

    def __init__(self):
        self.client_session = requests.Session()

    def HTTP_Request(self, url, GET=False, POST=False, Content=False, doctype=True, headers=None, headerclear=False, cookies=None, allow_redirects=False, encoding='utf-8', cf=False, cfdelay=0):
        """
            HTTP请求
        url: 网址 => 字符串
        GET: 请求类型GET,POST选其一 => bool
        POST: 请求类型GET,POST选其一 => bool
        doctype: 清理HTML DOCTYPE 头 => bool
        headers: 请求头 => dict
        cookies: cookies = dict
        allow_redirects: 遇到302请求重定向设置 => bool
        encoding: 字符集 => utf-8 gbk...
        cf: Cloudflare 防火墙模式 => bool
        delay: Cloudflare 防火墙模式 延时 单位秒 = int
        """
        if url == '':
            return {"issuccess": False, "error": "请求网址不能是空", "status_code": '', "html": ''}
        if GET and POST:
            return {"issuccess": False, "error": "明确请求类型HTTP_REQUEST(URL,GET=True,....)或HTTP_REQUEST(URL,POST=True,....)", "status_code": '', "html": ''}
        if not GET and not POST:
            GET = True

        try:
            if headerclear:                
                self.client_session.headers.clear()
            if not headers is None:
                self.client_session.headers.update(headers)
            if not cookies is None:
                self.client_session.cookies = requests.utils.cookiejar_from_dict(cookies)
            
            if cf:
                if cfdelay > 0:
                    scraper = cfscrape.create_scraper(
                        sess=self.client_session, delay=cfdelay)
                else:
                    scraper = cfscrape.create_scraper(
                        sess=self.client_session)
                if GET:
                    response = scraper.get(
                        url, allow_redirects=allow_redirects)
                else:
                    response = scraper.post(
                        url, allow_redirects=allow_redirects)
            else:
                if GET:
                    response = self.client_session.get(
                        url, allow_redirects=allow_redirects)
                else:
                    response = self.client_session.post(
                        url, allow_redirects=allow_redirects)


            if not encoding == '':
                response.encoding = encoding

            if response.status_code == 200:
                if Content == True:
                    return {"issuccess": True, "error": '', "status_code": response.status_code, "html": '', "content": response.content,
                        "headers": self.client_session.headers, "cookies": self.client_session.cookies}
                else:
                    text = ''
                    if doctype:
                        text = response.text.replace('\r', '').replace(
                            '\n', '').replace('\r\n', '')
                        text = text.replace('<?xml version="1.0" encoding="UTF-8"?>',
                                            '').replace('<!DOCTYPE html>\n', '')
                        text = text.replace(
                            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"', '')
                        text = text.replace(
                            '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">', '')
                    else:
                        text = response.text

                return {"issuccess": True, "error": '', "status_code": response.status_code, "html": text, "content":'',
                        "headers": self.client_session.headers, "cookies": self.client_session.cookies}
            else:
                return {"issuccess": False, "error": '', "status_code": response.status_code, "html": ''}
        except Exception as ex:
            return {"issuccess": False, "error": ex, "status_code": '', "html": ''}

