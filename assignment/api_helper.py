import requests

try:
    import json
except ImportError:
    import simplejson as json

VERSION = "v1"
BASE_URL = "https://api.plivo.com"

class API(object):
    def __init__(self, auth_id, auth_token, url=BASE_URL, version=VERSION):
        self.version = version
        self.url = url.rstrip('/') + '/' + self.version
        self.auth_id = auth_id
        self.auth_token = auth_token
        self._api = self.url + '/Account/%s' % self.auth_id
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 '}
    

    def _request(self, method, path, data={}):
        path = path.rstrip('/') + '/'
        if method == 'POST':
            headers = {'content-type': 'application/json'}
            headers.update(self.headers)
            r = requests.post(self._api + path, headers=headers,
                              auth=(self.auth_id, self.auth_token),
                              data=json.dumps(data))
        elif method == 'GET':
            r = requests.get(self._api + path, headers=self.headers,
                             auth=(self.auth_id, self.auth_token),
                             params=data)
        
        content = r.content
        if content:
            try:
                response = json.loads(content.decode("utf-8"))
            except ValueError:
                response = content
        else:
            response = content
        return (r.status_code, response)

    def get_numbers(self, params=None):
        if not params: params = {}
        return self._request('GET', '/Number/', data=params)

    def search_phone_numbers(self, params=None):
        if not params: params = {}
        return self._request('GET', '/PhoneNumber/', data=params)

    def buy_phone_number(self, params=None):
        if not params: params = {}
        number = params.pop("number")
        return self._request('POST', '/PhoneNumber/%s/' % number, data=params)

    def get_live_calls(self, params=None):
        if not params: params = {}
        params['status'] = 'live'
        return self._request('GET', '/Call/', data=params)

    def get_live_call(self, params=None):
        if not params: params={}
        params['status'] = 'live'
        call_uuid = params.pop('call_uuid')
        return self._request('GET', '/Call/%s/' % call_uuid, data=params)

    def make_call(self, params=None):
        if not params: params = {}
        return self._request('POST', '/Call/', data=params)


