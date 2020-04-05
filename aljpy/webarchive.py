"""Docs: https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server"""
import requests
import json
import pandas as pd

def index(target):
    url = f'http://web.archive.org/cdx/search/cdx'
    r = requests.get(url, params={'url': target, 'output': 'json'}, headers={'User-Agent': ''})
    r.raise_for_status()

    raw = json.loads(r.content)
    if raw:
        return (pd.DataFrame(raw[1:], columns=raw[0])
                    .assign(timestamp=lambda df: pd.to_datetime(df.timestamp, format='%Y%m%d%H%M%S'))
                    .assign(date=lambda df: df.timestamp.dt.normalize()))
    else:
        return pd.DataFrame(columns=['urlkey', 'timestamp', 'original', 'mimetype', 'statuscode', 'digest', 'length', 'date'])

def snapshot(target, timestamp=None):
    url = f'http://web.archive.org/web/{timestamp:%Y%m%d%H%M%S}/{target}'
    r = requests.get(url)
    r.raise_for_status()
    return r.content 
