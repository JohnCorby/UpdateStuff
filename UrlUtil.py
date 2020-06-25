import os
import re

from cloudscraper import CloudScraper, CloudflareChallengeError
from requests import Response

from Download import SERVER_DIR


def join(*parts: str) -> str:
    """join `parts` with '/'"""
    parts = list(map(lambda x: x.replace('\\', '/').strip('/'), parts))
    return '/'.join(parts)


scraper = CloudScraper()


def get(url: str) -> Response:
    """get a response from `url`"""
    global scraper
    while True:
        try:
            return scraper.get(url)
        except CloudflareChallengeError:
            print("challenge error. retrying")
            scraper = CloudScraper()


def get_file_name(res: Response) -> str:
    """get file name from `res`"""
    # res will be after all redirects

    # check for valid filename in url
    name = os.path.basename(res.url)
    if name.endswith('.jar'):
        return name

    # check for filename in content-disposition header
    header = res.headers['content-disposition']
    if header:
        matches = re.findall(r'filename=(.*)', header)
        name = matches[0]
        name = name.strip('"')
        if name.endswith('.jar'):
            return name


def strip_version(name: str) -> str:
    """remove version info from `path`"""
    name, ext = os.path.splitext(name)
    name = re.sub(r'[\d.]|snapshot', '', name, flags=re.IGNORECASE)
    return name + ext


def remove_existing(path: str):
    """
    find existing file and remove it
    checks for name without version
    """
    dir = os.path.dirname(path)

    for existing in os.listdir(dir):
        if not existing.endswith('jar'): continue
        existing = join(dir, existing)

        if strip_version(existing) == strip_version(path):
            print('removing existing', existing)
            os.remove(existing)
            return


PLUGIN_DIR = f'{SERVER_DIR}/plugins'


def download(url: str, dir=PLUGIN_DIR, name: str = None):
    """
    download file `name` to `dir` from `res`
    or dont if version is the same
    """
    res = get(url)
    if not name:
        name = get_file_name(res)
    path = join(dir, name)

    print('downloading', res.url, 'to', path)
    os.makedirs(dir, exist_ok=True)
    remove_existing(path)
    with open(path, 'wb') as f:
        f.write(res.content)
    print('done')
    print()
