import os
import logging
import requests


logging.basicConfig()
logger = logging.getLogger('upkquake-util')


def mkdir_if_notexists(path):
    """ just don't crash if dir is there please """
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def download_file(url, output_path):
    r = requests.get(url, stream=True)  # stream = True is important
    with open(output_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return output_path
