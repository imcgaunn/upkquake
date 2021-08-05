import logging
import os

import upkquake.constants as constants
import upkquake.util as util

logger = logging.getLogger("upkquake-assets")


Q2_ARCHIVE_ZIP = {
    "url": constants.Q2_ARCHIVE_URL,
    "checksum": constants.Q2_ARCHIVE_SHA256,
    "output_path": constants.DEFAULT_ZIP_PATH,
}

Q2_YAMAGI_PATCH = {
    "url": constants.Q2_YAMAGI_PATCH_URL,
    "checksum": constants.Q2_YAMAGI_PATCH_SHA256,
    "output_path": constants.DEFAULT_PATCH_PATH,
}

ALL = [Q2_ARCHIVE_ZIP, Q2_YAMAGI_PATCH]


def asset_on_disk(asset_info):
    return os.path.exists(asset_info["output_path"])


def download_with_cache(asset_info):
    output_path = asset_info["output_path"]
    if asset_on_disk(asset_info):
        if verify(asset_info):
            logger.debug(f"cached copy at {output_path} valid, can skip download")
            return output_path
    return download(asset_info)


def download(asset_info):
    output_path = asset_info["output_path"]
    asset_url = asset_info["url"]
    util.download_file(asset_url, output_path)
    if not verify(asset_info):
        msg = f"something went wrong downloading asset {asset_info}"
        raise RuntimeError(msg)
    return output_path


def verify(asset_info):
    expected_checksum = asset_info["checksum"]
    path = asset_info["output_path"]
    actual_checksum = util.hash_large_file(path)
    return actual_checksum == expected_checksum
