import os
import requests

class Session():
    """A Kalshi session.  All API requests are defined on this class.

       :param str email: The email you use to log in.  (This can also be configured with the KALSHI_EMAIL environment variable.)
       :param str password: The password you use to log in.  (This can also be configured with the KALSHI_PASSWORD environment variable.)
       :param str endpoint: The Kalshi API endpoint.  Defaults to the public v1 API.
"""
    def __init__(self, email=None, password=None,
                 endpoint='https://trading-api.kalshi.com/v1'):
        if email is None:
            if 'KALSHI_EMAIL' not in os.environ:
                raise RuntimeError(
                    "kalshi.Session needs to know your email.  "+
                    "Either provide `email` as a keyword argument "+
                    "or set `KALSHI_EMAIL` in the environment.")
            email = os.environ['KALSHI_EMAIL']
        if password is None:
            if 'KALSHI_PASSWORD' not in os.environ:
                raise RuntimeError(
                    "kalshi.Session needs to know your password.  "+
                    "Either provide `password` as a keyword argument "+
                    "or set `KALSHI_PASSWORD` in the environment.")
            password = os.environ['KALSHI_PASSWORD']
        self.endpoint = endpoint

        res = requests.post(endpoint+'/log_in', json={'email': email, 'password': password})
        if res.status_code != 200:
            raise RuntimeError('kalshi.Session failed to log in (%s) (%s)' %
                               (res.status_code, res.text))

        parsed = res.json()
        self.token = parsed['token']
        self.user_id = parsed['user_id']

    def post(self, path, obj=None):
        if obj is not None and obj != {}:
            res = requests.post(self.endpoint+path, json=obj, headers={'Authorization': self.token})
        else:
            res = requests.post(self.endpoint+path, headers={'Authorization': self.token})
        if res.status_code != 200:
            raise RuntimeError('Error from Kalshi API (%s) (%s)' % (res.status_code, res.text))
        return res.json()

    def get(self, path, obj=None):
        if obj is not None and obj != {}:
            res = requests.get(self.endpoint+path, json=obj, headers={'Authorization': self.token})
        else:
            res = requests.get(self.endpoint+path, headers={'Authorization': self.token})
        if res.status_code != 200:
            raise RuntimeError('Error from Kalshi API (%s) (%s)' % (res.status_code, res.text))
        return res.json()

