import re
from os.path import basename
from pprint import pformat

from pyquery import PyQuery

from Download import PLUGIN_DIR, SERVER_DIR
from UrlUtil import get, urljoin, download


def server():
    """download server jar"""
    print('downloading server jar')
    download('https://papermc.io/ci/job/Paper-1.15/lastSuccessfulBuild/artifact/paperclip.jar',
             SERVER_DIR, 'server.jar')
    print()


def plugin(url: str):
    """download plugin jar"""
    print('downloading plugin from', url)
    download(url, PLUGIN_DIR)
    print()


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


def jenkins(url: str, *patterns: str):
    """download plugin from jenkins `url`, looking for files that match any `patterns` (case insensitive)"""
    print('jenkins on', url)

    # find file list with latest releases
    d = PyQuery(get(url).content)
    file_urls = d('.fileList a[href$=jar]')
    file_urls = list(map(lambda x: urljoin(url, x.attrib['href']), file_urls))
    print('got files', pformat(list(map(lambda x: basename(x), file_urls))))

    # match to patterns and download
    matches = set()
    for pattern in patterns:
        for file_url in file_urls:
            if re.fullmatch(pattern, basename(file_url), re.IGNORECASE):
                print('pattern', pattern, 'matched', basename(file_url))
                matches.add(file_url)

    for match in matches:
        plugin(match)
