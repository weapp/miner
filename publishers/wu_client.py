import urllib, urllib2
import json

class WuClient:
    def __init__(self, client_id, client_secret, host="http://localhost:9292", token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.host = host
        self._build_opener()
        self.set_token(token)
        self._me = None

    def _build_opener(self):
        self.opener = urllib2.build_opener()
        # opener.addheaders = [('User-agent', 'Mozilla/5.0'),('ACCEPT-ENCODING','gzip;q=1.0,deflate;q=0.6,identity;q=0.3'), ("ACCEPT","*/*")]

    def set_token(self, token):
        self.token = token
        if token:
            self.opener.addheaders = [("Authorization", "OAuth %s" % token)]

    def auth(self, username, password):
        credentials = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": username,
            "password": password,
            "grant_type":"password",
            "scope":"read write",
        }
        # query = urllib.urlencode(credentials)
        try:
            r = self.open("/oauth/authorize", credentials)
        except Exception as e:
            print e
            return False
        self.set_token(r['access_token'])
        return True

    def open(self, path="/", query=None):
        # url = "%s%s" % (self.host, path)
        # r = self.opener.open(url, query)
        # return json.loads(r.read())
        if query:
            return self.post(path, query)
        else:
            return self.get(path)

    def get(self, path):
        return self._open("GET", path)

    def post(self, path, data):
        return self._open("POST", path, data)

    def put(self, path, data):
        return self._open("PUT", path, data)

    def _open(self, verb, path, data=None):
        # opener = urllib2.build_opener(urllib2.HTTPHandler)
        
        url = "%s%s" % (self.host, path)

        if data:
            data = urllib.urlencode(data)

        request = urllib2.Request(url, data=data)
        
        request.get_method = lambda: verb.upper()
        r = self.opener.open(request)
        return json.loads(r.read())

    def me(self):
        if not self._me:
            self._me = self.open("/api/me")        
        return self._me

    def user_id(self):
        return self.me()["id"]

    def new_wu(self, data):
        return self.post('/api/wbs', data)

    def update_value(self, wu, value):
        path = "/api/users/%s/wbs/%s" % (self.user_id(), wu)
        return self.put(path, {'data': value})
