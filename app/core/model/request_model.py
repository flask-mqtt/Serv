import json


class RequestModel:
    """
        作用为是的每一个request请求都带有token信息
        对应的vue src/utils/request.js 
        // request interceptor
        service.interceptors.request.use(
        config => {
            // do something before request is sent

            if (store.getters.token) {
            // let each request carry token
            // ['X-Token'] is a custom headers key
            // please modify it according to the actual situation
            config.headers['X-Token'] = getToken() //需要修改的地方 替换为 TorrentSubscribeTools-Token
            }
            return config
        },
        error => {
            // do something with request error
            console.log(error) // for debug
            return Promise.reject(error)
        }
        )
    """
    token = ''
    data = {}

    def __init__(self, request):
        self.token = request.headers.get("X-Token")
        json_str = request.get_data(as_text=True)
        if json_str is not None and json_str != '':
            self.data = json.loads(json_str)
        else:
            self.data = {}
