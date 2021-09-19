import hashlib
import logging
import os

import requests

import upkquake.constants as constants

logger = logging.getLogger("upkquake-util")


def mkdir_if_notexists(path):
    """just don't crash if dir is there please"""
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def hash_large_file(path, chunksize=constants.HASH_CHUNK_SIZE):
    """computes a sha256 digest of a large file by reading (at most) chunksize
    chunks at a time and feeding them to the hasher.
    """
    with open(path, "rb") as lf:
        return hash_stream_chunked(lf, chunksize)


def hash_stream_chunked(stream, chunksize=constants.HASH_CHUNK_SIZE):
    hasher = hashlib.sha256()
    chunk = stream.read(chunksize)
    while chunk:
        hasher.update(chunk)
        chunk = stream.read(chunksize)
    return hasher.hexdigest()


def download_file(url, output_path):
    r = requests.get(url, stream=True)  # stream = True is important
    with open(output_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=constants.DOWNLOAD_CHUNK_BYTES):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return output_path


def spinning_cursor():
    while True:
        for cursor in "opzfghi":
            yield cursor
