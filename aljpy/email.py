"""To get this to work, you need to set up a mailgun account and then create a `~/.credentials/mailgun.json` file that looks like

```
{"region": "eu_or_us", "domain": "YOUR_DOMAIN", "key": "YOUR_KEY"}
```

The domain will be a huge hashed string unless you've set up a custom domain. You should set up a custom domain.
"""
import json
import requests
from io import BytesIO
from pathlib import Path

def credentials():
    return json.loads(Path('~/.credentials/mailgun.json').expanduser().read_text())

def root():
    return f'https://api.{credentials()["region"]}.mailgun.net/v3/{credentials()["domain"]}'

def destination(emails):
    if emails is None:
        domain = credentials()["domain"]
        domain = domain[3:] if domain.startswith('mg.') else domain
        return [f'dev@{domain}']
    elif isinstance(emails, str):
        return [emails]
    else:
        return emails

def send(subject, content=' ', to=None, sender='python', attachments={}):
    data = {
        'from': f'{sender}@{credentials()["domain"]}',
        'to': destination(to),
        'subject': subject,
        'text': content}
    files = [('attachment', (k, BytesIO(v))) for k, v in attachments.items()]
    r = requests.post(
                f'{root()}/messages',
                auth=('api', credentials()['key']),
                data=data,
                files=files)
    r.raise_for_status()