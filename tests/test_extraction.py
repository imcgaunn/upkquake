import concurrent.futures
import logging
import os
import pprint
import re
import shutil
import tempfile
import time
import zipfile

import pytest

import upkquake.extraction as extraction

logger = logging.getLogger("test-extraction")


@pytest.mark.skip
def test_download_in_threadpool_not_blocking():
    download_handle = extraction.start_download_in_threadpool()
    print("did this happen???")
    while download_handle.running():
        print("still downloadin...")


@pytest.mark.skip
def test_download_in_threadpool_local_creation():
    with concurrent.futures.ThreadPoolExecutor() as tp:
        hh = tp.submit(dummy_long_task)
        h2 = tp.submit(dummy_long_task)
        while any([hh.running(), h2.running()]):
            print("tasks goin!")
            time.sleep(1)
        results = concurrent.futures.as_completed([hh, h2])
        pprint.pprint(results)


@pytest.fixture(scope="function")
def test_temp_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture(scope="function")
def example_zip_file(test_temp_dir):
    example_files = []
    # put some files in test_temp_dir that we can add to the zipfile
    # and verify that they can be retrieved
    for i in range(10):
        ep = os.path.join(test_temp_dir, f"examplefile{i}.txt")
        with open(ep, "w") as f:
            f.write("great contents")
        example_files.append(ep)

    zip_path = os.path.join(test_temp_dir, "example.zip")
    with zipfile.ZipFile(zip_path, "w") as z:
        for ef in example_files:
            z.write(ef, arcname=os.path.basename(ef))
    yield zip_path


def test_extract_with_7z(example_zip_file, test_temp_dir):
    extract_dir = os.path.join(test_temp_dir, "extracted_zip")
    extraction.extract_zip_with_7z(example_zip_file, extract_dir)
    extracted_files = os.listdir(extract_dir)
    for i in range(10):
        assert f"examplefile{i}.txt" in extracted_files


@pytest.mark.skip("this test takes too long to run all the time")
def test_unpack_and_split(test_temp_dir):
    # copy quake2 zip into test temp dir
    home_dir = os.getenv("USERPROFILE") if os.name == "nt" else os.getenv("HOME")
    upkquake_cache_dir = os.path.join(home_dir, ".cache", "upkquake")
    dest_path = os.path.join(test_temp_dir, "Quake II.zip")
    output_dir = os.path.join(test_temp_dir, "unpacked_cd")
    logger.info("copying quake II zip to temp dir for fun and testing")
    shutil.copy(os.path.join(upkquake_cache_dir, "Quake II.zip"), dest_path)
    data_track, cdr_files = extraction.unpack_zip_and_split_cd_tracks(
        dest_path, output_dir
    )
    assert data_track
    assert len(cdr_files)


def dummy_long_task():
    time.sleep(10)


def test_cdr_name_to_ogg_name(test_temp_dir):
    example_cdr_names = [
        "Quake 2.iso07.cdr",
        "Quake 2.iso06.cdr",
        "Quake 2.iso04.cdr",
        "Quake 2.iso10.cdr",
        "Quake 2.iso11.cdr",
        "Quake 2.iso05.cdr",
        "Quake 2.iso02.cdr",
        "Quake 2.iso03.cdr",
        "Quake 2.iso08.cdr",
        "Quake 2.iso09.cdr",
    ]
    for cdr_name in example_cdr_names:
        ogg_name = extraction.cdr_name_to_ogg_name(cdr_name, test_temp_dir)
        logger.info(f"ogg: {ogg_name}")
        assert re.match(r".*(\d){2}.ogg", ogg_name)
