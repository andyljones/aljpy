import requests
from tqdm.auto import tqdm
from io import BytesIO

def download(url):
    bs = BytesIO()
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total = r.headers.get('Content-Length', None)
        with tqdm(total=total, unit_scale=True, unit_divisor=1024, unit='B') as pbar:
            for chunk in r.iter_content(chunk_size=2**20): 
                pbar.update(len(chunk))
                bs.write(chunk)
    return bs.getvalue()
        