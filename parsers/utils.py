import os
from urllib.parse import urlparse


def read_links_txt(filename):
    with open(filename) as f:
        return f.read().split('\n')


def get_file_name_from_url(url):
    return os.path.basename(urlparse(url).path)

