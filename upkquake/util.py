import os
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


def download_file(url, output_path):
    r = requests.get(url, stream=True)  # stream = True is important
    with open(output_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=constants.DOWNLOAD_CHUNK_BYTES):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return output_path


def download_asset_with_cache(asset_info):
    output_path = asset_info["output_path"]
    asset_url = asset_info["url"]
    asset_checksum = asset_info["checksum"]
    if os.path.exists(output_path):
        logger.debug(f"{output_path} found, checking integrity")
        # TODO: verify downloaded file using passed checksum
        # if verify_asset(path, asset_info):
        logger.debug(f"cached copy at {output_path} valid, can skip download")


def spinning_cursor():
    while True:
        for cursor in "opzfghi":
            yield cursor
