import os
import hashlib
import logging
import requests

import upkquake.constants as constants


logging.basicConfig()
logger = logging.getLogger("upkquake-util")


def mkdir_if_notexists(path):
    """ just don't crash if dir is there please """
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


def download_asset_with_cache(asset_info):
    output_path = asset_info["output_path"]
    if os.path.exists(output_path):
        logger.debug(f"{output_path} found, checking integrity")

        if verify_asset(asset_info):
            logger.debug(f"cached copy at {output_path} valid, can skip download")
            return output_path
    return download_asset(asset_info)


def download_asset(asset_info):
    output_path = asset_info["output_path"]
    asset_url = asset_info["url"]
    download_file(asset_url, output_path)
    if not verify_asset(asset_info):
        msg = f"something went wrong downloading asset {asset_info}"
        raise RuntimeError(msg)
    return output_path


def verify_asset(asset_info):
    expected_checksum = asset_info["checksum"]
    path = asset_info["output_path"]
    actual_checksum = hash_large_file(path)
    return actual_checksum == expected_checksum


def spinning_cursor():
    while True:
        for cursor in "opzfghi":
            yield cursor
