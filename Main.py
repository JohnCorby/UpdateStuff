from os import listdir

from Download import manual_download, SERVER_DIR
from UrlUtil import download


def server():
    """download server jar"""
    print('downloading server')
    download('https://papermc.io/ci/job/Paper-1.15/lastSuccessfulBuild/artifact/paperclip.jar',
             SERVER_DIR, 'server.jar')


def auto_download():
    """automatically download using url files"""
    print('auto downloading from url files')
    listdir(SERVER_DIR)


if __name__ == '__main__':
    server()
    auto_download()
    print('manually downloading')
    manual_download()
    print('finished')
