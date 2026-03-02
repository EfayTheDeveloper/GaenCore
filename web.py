import urllib.request

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

def download(url, file):
    urllib.request.urlretrieve(url, file)
