import re
from os.path import basename, join

import requests
from cloudscraper import CloudScraper


def urljoin(base: str, leaf: str) -> str:
    """join 2 parts of urls with '/'"""
    base = base.replace('\\', '/').strip('/')
    leaf = leaf.replace('\\', '/').strip('/')
    return f'{base}/{leaf}'


scraper = CloudScraper()


def get(url: str) -> requests.Response:
    """get a response from `url`"""
    # just always use cloudflare scraper, even if not required
    return scraper.get(url)


def get_file_name(res: requests.Response) -> str:
    """get file name from `res`"""
    # res will be after all redirects

    # check for valid filename in url
    name = basename(res.url)
    if name.endswith('.jar'):
        return name

    # check for filename in content-disposition header
    header = res.headers['content-disposition']
    if header:
        matches = re.findall(r'filename="(.*)"', header)
        name = matches[0]
        if name.endswith('.jar'):
            return name


def download(url: str, dir: str, name: str = None):
    """download file `name` to `dir` from `res`"""
    res = get(url)
    if not name:
        name = get_file_name(res)
    path = join(dir, name)

    print('downloading', res.url, 'to', path)
    with open(path, 'wb') as f:
        f.write(res.content)
    print('done')
