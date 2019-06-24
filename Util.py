import re
from os.path import basename, join
from pprint import pformat
from typing import Pattern

import cfscrape
import requests
from pyquery import PyQuery

PLUGIN_DIR = '../plugins'


def urljoin(base: str, leaf: str) -> str:
    """join 2 parts of urls with '/'"""
    return base.strip('/') + '/' + leaf.strip('/')


def get(url: str) -> (requests.Response, str):
    """get url, disabling ssl verification if needed"""
    try:
        return requests.get(url)
    except requests.exceptions.SSLError:
        return requests.get(url, verify=False)


def get_file_name(res: requests.Response) -> str:
    """get file name from `res`"""
    # NOTE: res will be data after all redirects

    # check for valid filename in url
    name = basename(res.url)
    if name.endswith('.jar'):
        return name

    # check for filename in content-disposition header
    header = res.headers['content-disposition']
    if header:
        matches = re.findall(r'[^="]+?\.jar', header)
        if matches:
            return matches[0]


def download(res: requests.Response, dir: str, name: str = None):
    """download file `name` to `dir` from `res`"""
    if not name:
        name = get_file_name(res)
    path = join(dir, name)

    print('downloading', res.url, 'to', path)
    with open(path, 'wb') as f:
        f.write(res.content)
    print('done')


def jenkins(url: str, *patterns: Pattern):
    """download plugin from jenkins site `url`, looking for files that match each pattern in `patterns`"""
    print('jenkins on', url)
    d = PyQuery(get(url).content)

    # find file list with latest releases
    file_urls = d('.fileList a[href$=".jar"]')
    file_urls = map(lambda e: urljoin(url, e.attrib['href']), file_urls)
    file_urls = list(file_urls)
    print('got files', pformat(file_urls), sep='\n')

    # match to patterns and download
    matches = []
    for p in patterns:
        for u in file_urls:
            if p.fullmatch(basename(u)):
                matches.append(u)
                break
    print('got matches', pformat(matches), sep='\n')

    for m in matches:
        download(get(m), PLUGIN_DIR)


def spigot(url: str):
    """download plugin from spigot `url`"""
    print('spigot on', url)
    d = PyQuery(get(url).content)

    # get href download button links to
    dl_url = d('.downloadButton a').attr('href')
    dl_url = urljoin(url, basename(dl_url))
    print('got dl url', dl_url)

    # go to that link using the cloudflare bypass thing
    download(cfscrape.create_scraper().get(dl_url), PLUGIN_DIR)
