# ---------------------------------------------------------------------
# ---------------------------- neobots --------------------------------
# ------------------------------txtsd----------------------------------
# ---------------------------------------------------------------------

"""Handles the account, login, and connections"""

import requests
import pickle
import re
import os


class NeoAccount:

    domain = 'http://www.neopets.com'
    images = 'http://images.neopets.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
    }

    def __init__(self, username, password, proxy='', pin=''):
        self.username = username
        self.password = password
        self.proxy = proxy
        self.pin = pin
        self.net_cache = 'cache'
        self.fname_pickle = '%s/%s.session' % (self.net_cache, self.username)

        if not os.path.exists(self.net_cache):
            os.makedirs(self.net_cache)
        if os.path.isfile(self.fname_pickle):
            with open(self.fname_pickle, 'rb') as file:
                self.session = pickle.load(file)
        else:
            self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount('http://', adapter)
        self.session.headers.update(self.headers)

        if (self.proxy != ''):
            self.session.proxies = {'http': 'http://' + self.proxy + '/'}

    def get(self, url, param={}, referer='', head={}):
        if url[0] == '/':
            url = NeoAccount.domain + url
        if referer != '':
            if referer[0] == '/':
                referer = NeoAccount.domain + referer
            head['Referer'] = referer
        result = self.session.get(
            url,
            params=param,
            headers=head,
        )
        return result

    def post(self, url, data={}, param={}, referer='', head={}):
        if url[0] == '/':
            url = NeoAccount.domain + url
        if referer != '':
            if referer[0] == '/':
                referer = NeoAccount.domain + referer
            head['Referer'] = referer
        result = self.session.post(
            url,
            params=param,
            data=data,
            headers=head,
        )
        return result

    def login(self):
        result = self.get('/inventory.phtml')
        if 'login/index.phtml' in result.url:
            print('Not logged in. Logging in.')
            result = self.post(
                '/login.phtml',
                data={
                    'username': self.username,
                    'password': self.password,
                    'destination': '%2Findex.phtml',
                }
            )
            if 'badpassword' in result.url:
                print('Bad password!')
                return False, result.url
            elif 'hello' in result.url:
                print('Birthday locked!')
                return False, result.url
            elif 'login' in result.url:
                print('Frozen!')
                return False, result.url
            elif 'index' in result.url:
                print('Successfully logged in!')
                with open(self.fname_pickle, 'wb') as file:
                    pickle.dump(self.session, file, pickle.HIGHEST_PROTOCOL)
                return True
        elif re.search('user=' + self.username, result.text):
            print('Already logged in!')
            return True
