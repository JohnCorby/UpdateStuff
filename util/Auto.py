import glob
import re
import traceback

from Manual import PLUGIN_DIR, SERVER_DIR
from util.Download import auto
from util.Util import join, split


def auto_download():
    """automatically download using url files"""
    print('auto downloading from url files')
    for server_path in glob.iglob(join(SERVER_DIR, "*.url")):
        download_from_file(server_path)
    for plugin_path in glob.iglob(join(PLUGIN_DIR, "*.url")):
        download_from_file(plugin_path)


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
