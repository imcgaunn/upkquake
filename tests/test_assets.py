import hashlib
import logging
import os
import secrets
import shutil
import tempfile
import unittest.mock as mock

import pytest

import upkquake.assets as assets
import upkquake.util as util

logger = logging.getLogger("test-assets")
LOWERCASE_CHARS = [chr(n) for n in range(ord("a"), ord("z") + 1)]


def _gen_test_asset(tempdir):
    # assets created here get cleaned up when the tempdir is removed
    # by the tempdir_assets fixture.
    pbytes = secrets.token_bytes(512)
    contents = pbytes * 10
    asset_checksum = hashlib.sha256(contents).hexdigest()
    random_name = "".join(secrets.choice(LOWERCASE_CHARS) for _ in range(10))
    logger.debug(f"naming asset: {random_name}")
    with open(os.path.join(tempdir, random_name), "wb") as f:
        f.write(contents)
    return {
        "url": f"http://localhost/assets/{random_name}",
        "checksum": asset_checksum,
        "output_path": os.path.join(tempdir, random_name),
    }


@pytest.fixture(scope="function")
def tempdir_assets():
    tempdir_loc = tempfile.mkdtemp()
    example_assets = [_gen_test_asset(tempdir_loc) for _ in range(8)]
    yield example_assets
    if os.path.exists(tempdir_loc):
        logger.debug(f"cleanup: removing {tempdir_loc}")
        shutil.rmtree(tempdir_loc)


@pytest.fixture(scope="function")
def patch_download_file(tempdir_assets):
    def _mock_download_file(url, output_path):
        try:
            match = [a for a in tempdir_assets if a["url"] == url][0]
            return match["output_path"]
        except (IndexError, KeyError):
            return "no match"
        return "no match"

    with mock.patch(f"{util.__name__}.download_file") as mock_download_file:
        mock_download_file.side_effect = _mock_download_file
        yield mock_download_file


def test_download_with_cache_when_asset_cached(tempdir_assets, patch_download_file):
    for a in tempdir_assets:
        output_path = assets.download_with_cache(a)
        assert output_path
        # assert that download_file was _NOT_ called -- if resource is cached/valid
        # this should not be necessary.
        assert not patch_download_file.called


def test_download_with_cache_when_asset_not_cached(tempdir_assets, patch_download_file):
    # force asset_on_disk to return false so assets will need to be fetched again
    test_asset = tempdir_assets[0]
    with mock.patch(f"{assets.__name__}.asset_on_disk") as mock_on_disk:
        mock_on_disk.return_value = False
        output_path = assets.download_with_cache(test_asset)
        assert output_path
        # download file _should_ be called in this case.
        assert patch_download_file.called
