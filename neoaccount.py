import requests
import pickle
import logging
import re
from pathlib import Path


class NeoAccount:
    domain = 'http://www.neopets.com'
    firefoxUA = 'Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'
    chromeUA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.17 Safari/537.36'

    def __init__(self, config):
        self.username = config['username']
        self.password = config['password']
        self.proxy = config['proxy']
        self.useragent = config['useragent']
        self.userhash = self.username.encode('utf-8')
        self.cachefile = Path('.cache' + '/' + self.username)

        # Apply headers based on browser in useragent
        if 'Firefox' in self.useragent:
            self.headers = {
                'User-Agent': self.useragent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
            }
        elif 'Chrome' in self.useragent:
            self.headers = {
                'User-Agent': self.useragent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
            }

        # Setup logger
        self.logger = logging.getLogger('neobots.NeoAccount')

        # Load cookies or create a session
        Path('.cache').mkdir(exist_ok=True)
        if Path.is_file(self.cachefile):
            with open(self.cachefile, 'rb') as f:
                self.session = pickle.load(f)
        else:
            self.session = requests.Session()

        # Set headers
        self.session.headers = self.headers

        # Set proxy if exists
        if (self.proxy != ''):
            self.session.proxies = {'http': 'http://{}/'.format(self.proxy)}

    # GET
    def get(self, url, params={}, referer='', headers={}):
        if url[0] == '/':
            url = self.domain + url
        if referer != '':
            if referer[0] == '/':
                referer = self.domain + referer
            headers['Referer'] = referer
        result = self.session.get(url, params=params, headers=headers)
        return result

    # POST
    def post(self, url, data={}, params={}, referer='', headers={}):
        headers['Origin'] = self.domain
        if url[0] == '/':
            url = self.domain + url
        if referer != '':
            if referer[0] == '/':
                referer = self.domain + referer
            headers['Referer'] = referer
        result = self.session.post(url, params=params, data=data, headers=headers)
        return result

    # XHR
    def xhr(self, url, data={}, params={}, referer='', headers={}):
        headers['Origin'] = self.domain
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['Accept'] = '*/*'
        if url[0] == '/':
            url = self.domain + url
        if referer != '':
            if referer[0] == '/':
                referer = self.domain + referer
            headers['Referer'] = referer
        result = self.session.post(url, params=params, data=data, headers=headers)
        return result

    # Login
    def login(self):
        self.logger.debug(account.username + ': Logging in')
        result = self.get('http://www.neopets.com/index.phtml')
        match = re.search(
            'Welcome, <a href="/userlookup\.phtml\?user=(?P<username>.+?)">',
            result.text)
        if match:
            if match['username'] == self.username:
                self.logger.info(self.username + ': Already logged in!')
                return True
        result = self.get(
            'http://www.neopets.com/login/',
            referer='/index.phtml'
        )
        result = self.post(
            'http://www.neopets.com/login.phtml',
            data={
                'username': self.username,
                'password': self.password,
                'destination': 'http://www.neopets.com/index.phtml'
            },
            referer='/login/'
        )
        if 'badpassword' in result.url:
            self.logger.error(self.username + ': Bad Password!')
            return False
        elif 'hello' in result.url:
            self.logger.error(self.username + ': Birthday Locked!')
            return False
        elif 'login' in result.url:
            self.logger.error(self.username + ': Account Frozen!')
            return False
        elif 'index' in result.url:
            with open(self.cachefile, 'wb') as f:
                pickle.dump(self.session, f, pickle.HIGHEST_PROTOCOL)
            self.logger.info(self.username + ': Logged in!')
            return True
