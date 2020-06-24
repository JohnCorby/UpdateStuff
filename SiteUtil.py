import re
from os.path import basename
from pprint import pformat

from pyquery import PyQuery

from UrlUtil import get, urljoin, download


def auto(url: str):
    """download `url` to `dir`, doing specific automation based on what `url` is"""
    print('auto on', url)
    if 'https://www.spigotmc.org/resources/' in url:
        spigot(url)
    elif 'https://dev.bukkit.org/projects/' in url:
        bukkit(url)
    elif '/job/' in url:
        jenkins(url)
    else:
        download(url)


def bukkit(url: str):
    """download plugin from bukkit `url`"""
    print('bukkit on', url)

    dl_url = urljoin(url, 'files/latest')
    print('dl url is', dl_url)

    download(dl_url)


def spigot(url: str):
    """download plugin from spigot `url`"""
    print('spigot on', url)
    d = PyQuery(get(url).content)

    # get href download button links to
    dl_url = d('.downloadButton a').attr('href')
    dl_url = urljoin(url, basename(dl_url))
    print('got dl url', dl_url)

    download(dl_url)


def jenkins(url: str, *patterns: str):
    """download plugin from jenkins `url`, looking for files that contain any `patterns` (case insensitive)"""
    if not patterns: patterns = ['']
    print('jenkins on', url)

    # find urls ending in jar
    d = PyQuery(get(url).content)
    file_urls = d('a[href$=jar]')
    file_urls = list(map(lambda x: urljoin(url, x.attrib['href']), file_urls))
    print('got files', pformat(list(map(lambda x: basename(x), file_urls))))

    # match to patterns and download
    matches = set()
    for pattern in patterns:
        for file_url in file_urls:
            if re.match(pattern, basename(file_url), re.IGNORECASE):
                print(f'pattern "{pattern}" matched', basename(file_url))
                matches.add(file_url)

    for match in matches:
        download(match)
