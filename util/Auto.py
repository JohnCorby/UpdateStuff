import glob
import re
import traceback

from Manual import PLUGIN_DIR, SERVER_DIR
from util.Site import auto
from util.Util import join, split


def auto_download():
    """automatically download using url files"""
    print('auto downloading from url files')
    download_from_file(join(SERVER_DIR, 'server.url'))

    for path in glob.iglob(join(PLUGIN_DIR, "*.url")):
        download_from_file(path)


def download_from_file(path: str):
    """download from url file"""
    try:
        with open(path) as f:
            url = f.read()
        url = re.search(r'url=(.+)', url, flags=re.IGNORECASE | re.VERBOSE)
        url = url[1]
        print('got url', url)

        dir, name, ext = split(path)
        auto(url, dir, f'{name}.jar')
    except:
        traceback.print_exc()
