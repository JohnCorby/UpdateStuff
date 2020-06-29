"""
misc utils that dont depend on any other project files
helps prevent circular imports
"""
import glob
import os
import re
import traceback

from cloudscraper import CloudScraper, CloudflareChallengeError
from requests import Response


def split(path: str):
    """split `path` into dir, name, ext"""
    dir, name = os.path.split(path)
    name, ext = os.path.splitext(name)
    return dir, name, ext


def join(*parts: str):
    """join `parts` with '/'"""
    parts = list(map(lambda x: x.replace('\\', '/').strip('/'), parts))
    return '/'.join(parts)


scraper = CloudScraper()


def get(url: str):
    """get a response from `url`"""
    global scraper
    while True:
        try:
            return scraper.get(url)
        except CloudflareChallengeError:
            print("challenge error. retrying")


def get_file_name(res: Response):
    """get file name from `res`"""
    # res will be after all redirects

    # check for valid filename in url
    name = os.path.basename(res.url)
    if name.endswith('.jar'):
        return name

    # check for filename in content-disposition header
    header = res.headers.get('content-disposition')
    if header:
        name = re.search(r'filename=(.+)', header, flags=re.IGNORECASE | re.VERBOSE)
        name = name[1]
        name = name.strip('"')
        if name.endswith('.jar'):
            return name


def remove_existing(path: str):
    """find existing files and remove them"""
    dir, name, ext = split(path)

    # remove version info
    # format: hyphen, numbers with dots between them, optional hyphen and "SNAPSHOT"
    name = re.sub(r'- \d+(\.\d+)* (-snapshot)?', '', name, flags=re.IGNORECASE | re.VERBOSE)

    # find and try to remove existing files
    for existing in glob.iglob(join(dir, f'*{name}*{ext}')):
        print('removing existing', existing)
        try:
            os.remove(existing)
        except:
            traceback.print_exc()
