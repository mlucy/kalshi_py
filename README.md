This is a client for accessing Kalshi in Python.

`kalshi/session.py` is autogenerated using the script
`generate_session_py.py`.  I left it in source control so it would be
easy for people to pull and play with it.

Example usage:

```py
import kalshi
from pprint import pprint

s = kalshi.Session(email=..., password=...)
markets = s.get_markets_cached()['markets']
pprint(markets[0])
```

Docs: https://kalshi-py.readthedocs.io/en/latest/autoapi/kalshi/index.html

REST API spec: https://kalshi-public-docs.s3.amazonaws.com/KalshiAPI.html
