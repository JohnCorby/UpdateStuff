import os
import re
import traceback
from os.path import basename
from pprint import pformat

from pyquery import PyQuery

from Manual import PLUGIN_DIR
from util.Util import join, get, get_file_name, remove_existing


def auto(url: str, dir=PLUGIN_DIR, name: str = None):
    """download `url`, doing specific automation based on what `url` is"""
    print('auto on', url)
    try:
        try:
            download(url, dir, name)
            return
        except BadUrlError:
            if 'https://www.spigotmc.org/resources/' in url:
                spigot(url, dir, name)
            elif 'https://dev.bukkit.org/projects/' in url:
                bukkit(url, dir, name)
            elif '/job/' in url:
                jenkins(url, dir=dir, name=name)
            else:
                raise RuntimeError(f'cant figure out how to auto download {url}')
    except:
        traceback.print_exc()


def bukkit(url: str, dir=PLUGIN_DIR, name: str = None):
    """download from bukkit `url`"""
    print('bukkit on', url)

    dl_url = join(url, 'files/latest')
    print('dl url is', dl_url)

    try:
        download(dl_url, dir, name)
    except:
        traceback.print_exc()


def spigot(url: str, dir=PLUGIN_DIR, name: str = None):
    """download from spigot `url`"""
    print('spigot on', url)
    try:
        d = PyQuery(get(url).content)

        # get href download button links to
        dl_url = d('.downloadButton a').attr('href')
        dl_url = join(url, basename(dl_url))
        print('got dl url', dl_url)

        download(dl_url, dir, name)
    except:
        traceback.print_exc()


def jenkins(url: str, *patterns: str, dir=PLUGIN_DIR, name: str = None):
    """download from jenkins `url`"""
    if not patterns: patterns = ['']
    print('jenkins on', url)

    try:
        # find urls ending in jar
        d = PyQuery(get(url).content)
        file_urls = d('a[href$=".jar"]')
        file_urls = list(map(lambda x: join(url, x.attrib['href']), file_urls))
        print('got files', pformat(list(map(lambda x: basename(x), file_urls))))

        # match to patterns and download
        matches = set()
        for pattern in patterns:
            for file_url in file_urls:
                file_name = basename(file_url)
                if re.search(pattern, file_name, flags=re.IGNORECASE | re.VERBOSE):
                    print(f"pattern '{pattern}' matched", file_name)
                    matches.add(file_url)

        for match in matches:
            download(match, dir, name)
    except:
        traceback.print_exc()


class BadUrlError(Exception): pass


def download(url: str, dir=PLUGIN_DIR, name: str = None):
    """download file `name` to `dir` from `res`"""
    res = get(url)
    file_name = get_file_name(res)
    if not file_name: raise BadUrlError(f'{res.url} doesnt point to a jar file')
    if not name: name = file_name

    path = join(dir, name)
    os.makedirs(dir, exist_ok=True)
    remove_existing(path)
    print('downloading', res.url, 'to', path)
    with open(path, 'wb') as f:
        f.write(res.content)
    print('done')
    print()
