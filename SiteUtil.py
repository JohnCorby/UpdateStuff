from os.path import basename
from pprint import pformat
from typing import Pattern

from pyquery import PyQuery

from Download import PLUGIN_DIR, SERVER_DIR
from UrlUtil import get, urljoin, download


def server():
    """download server jar"""
    print('downloading server jar')
    download('https://papermc.io/ci/job/Paper-1.15/lastSuccessfulBuild/artifact/paperclip.jar',
             SERVER_DIR, 'server.jar')


def plugin(url: str):
    """download plugin jar"""
    print('downloading plugin from', url)
    download(url, PLUGIN_DIR)


def bukkit(url: str):
    """download plugin from bukkit `url`"""
    print('bukkit on', url)

    dl_url = urljoin(url, 'files/latest')
    print('dl url is', dl_url)

    plugin(dl_url)


def spigot(url: str):
    """download plugin from spigot `url`"""
    print('spigot on', url)
    d = PyQuery(get(url).content)

    # get href download button links to
    dl_url = d('.downloadButton a').attr('href')
    dl_url = urljoin(url, basename(dl_url))
    print('got dl url', dl_url)

    plugin(dl_url)


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
        plugin(m)
