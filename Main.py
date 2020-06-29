from Manual import manual_download
from util.Auto import auto_download

if __name__ == '__main__':
    auto_download()
    print('manually downloading')
    manual_download()
    print('finished')
