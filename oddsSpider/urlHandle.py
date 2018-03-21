import requests
import bs4


class urlHandler():
    def __init__(self,decode):
        self.decode=decode

    def get(self, **kwargs):
        self.res = requests.get(self.url, kwargs)

    def post(self, **kwargs):
        self.res = requests.post(self.url, kwargs)


class beautifulSoup(urlHandler):
    def __init__(self, url):
        self.url = url

    def beautifulSoup(self):
        self.soup = bs4.BeautifulSoup(self.res.content)

    def select(self, t):
        return self.soup.select(t)


class json(urlHandler):
    def __init__(self, url):
        self.url = url

    def json(self):
        self.json = self.res.json()


class text(urlHandler):
    def __init__(self, url):
        self.url = url

    def text(self):
        self.text = self.res.text
