# ---------------------------------------------------------------------
# ---------------------------- neobots --------------------------------
# ------------------------------txtsd----------------------------------
# ---------------------------------------------------------------------

"""Handles the account, login, and connections"""

import requests


class NeoAccount:

    domain = 'http://www.neopets.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
    }

    def __init__(self, username, password, proxy=""):
        self.username = username
        self.password = password
        self.proxy = proxy

        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount('http://', adapter)
        self.session.headers = self.headers

        if (self.proxy != ""):
            self.session.proxies = {'http': 'http://' + self.proxy + '/'}

    def get(self, url, param={}, referer='', head={}):
        if url[0] == '/':
            url = self.domain + url
        if referer != '':
            if referer[0] == '/':
                referer = self.domain + referer
            head['Referer'] = referer
        result = self.session.get(
            url,
            params=param,
            headers=head,
        )
        return result

    def post(self, url, data={}, param={}, referer='', head={}):
        if url[0] == '/':
            url = self.domain + url
        if referer != '':
            if referer[0] == '/':
                referer = self.domain + referer
            head['Referer'] = referer
        result = self.session.post(
            url,
            params=param,
            data=data,
            headers=head,
        )
        return result

    def login(self):
        self.result = self.session.get(
            'http://www.neopets.com/index.phtml', timeout=60)
        self.result = self.session.post('http://www.neopets.com/login.phtml',
                                        data={
                                            'username': self.username,
                                            'password': self.password,
                                            'destination': "http://www.neopets.com/index.phtml"}, timeout=60)
        print(self.result.url)
        if 'badpassword' in self.result.url:
            return False, 'Bad password'
        elif 'hello' in self.result.url:
            return False, 'Birthday locked'
        elif 'login' in self.result.url:
            return False, 'Frozen'
        elif 'index' in self.result.url:
            return True, 'Logged in'
