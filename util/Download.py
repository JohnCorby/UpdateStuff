import os

from Manual import PLUGIN_DIR
from util.Util import join, get, get_file_name, remove_existing


def download(url: str, dir=PLUGIN_DIR, name: str = None):
    """download file `name` to `dir` from `res`"""
    res = get(url)
    if not name:
        name = get_file_name(res)
    path = join(dir, name)

    os.makedirs(dir, exist_ok=True)
    remove_existing(path)
    print('downloading', res.url, 'to', path)
    with open(path, 'wb') as f:
        f.write(res.content)
    print('done')
    print()
