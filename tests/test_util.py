import io
import os
import secrets
import shutil
import tempfile

import pytest

import upkquake.util as util

TEST_CHUNK_SIZE = 4096


@pytest.fixture()
def large_file():
    # delete=False required due to windows not allowing multiple
    # open calls to an already open file - the workaround is to close
    # the temp file in the fixture before passing the file name around.
    lf = tempfile.NamedTemporaryFile(delete=False, mode="wb")
    for i in range(10000):
        lf.write(b"0x42" * (TEST_CHUNK_SIZE - 4))
    lf.close()
    yield lf.name
    # manually cleanup temp file
    if os.path.exists(lf.name):
        os.unlink(lf.name)


@pytest.fixture(scope="function")
def patch_download_asset(mocker, tempdir_assets):
    def _fake_download(url, output_path):
        try:
            match = [a for a in tempdir_assets if a["url"] == url][0]
            return match["output_path"]
        except (IndexError, KeyError):
            return "no match"
        return "no match"

    mocker.patch(f"{util.__name__}.download_file", new=_fake_download)


@pytest.fixture(scope="function")
def tempdir_assets():
    tempdir_loc = tempfile.mkdtemp()
    example_assets = []
    for asset_name in {
        "test_asset_one.dat",
        "test_asset_two.dat",
        "test_asset_three.dat",
    }:
        asset_path = os.path.join(tempdir_loc, asset_name)
        with open(asset_path, "wb") as f:
            pbytes = secrets.token_bytes(512)
            contents = pbytes * 10
            f.write(contents)
            # save checksum for use in example_asset_infos fixture
            checksum = util.hash_stream_chunked(io.BytesIO(contents))
            example_assets.append(
                {
                    "url": f"http://localhost:8888/{asset_name}",
                    "checksum": checksum,
                    "output_path": asset_path,
                }
            )
    yield tempdir_loc, example_assets
    # clean up after ourselves
    shutil.rmtree(tempdir_loc, ignore_errors=True)


def test_hash_large_file(large_file):
    hh = util.hash_large_file(large_file, TEST_CHUNK_SIZE)
    assert hh == "f03913edeb38a9569ccd6588b6338e58eb56fdcf0e8cecd0193cf68f180d6be1"


def test_download_asset_with_cache_asset_cached(patch_download_asset, tempdir_assets):
    _, assets = tempdir_assets
    for asset_info in assets:
        util.download_asset_with_cache(asset_info)


def test_download_asset_with_cache_asset_not_cached():
    pass


def test_verify_asset_valid(tempdir_assets):
    _, assets = tempdir_assets
    for a in assets:
        assert util.verify_asset(a)


def test_verify_asset_invalid(tempdir_assets):
    _, assets = tempdir_assets
    # corrupt checksum for asset so validate should fail
    corrupted_asset = assets[0]
    corrupted_asset[
        "checksum"
    ] = "87428fc522803d31065e7bce3cf03fe475096631e5e07bbd7a0f25c7"
    assert not util.verify_asset(corrupted_asset)
