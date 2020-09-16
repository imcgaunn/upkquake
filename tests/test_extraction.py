import pytest
import tempfile
import concurrent.futures
import upkquake.extraction as extraction
import time
import pprint


TEST_CHUNK_SIZE = 4096


@pytest.fixture()
def large_file():
    lf = tempfile.NamedTemporaryFile()
    for i in range(10000):
        lf.write(b"0x42" * (TEST_CHUNK_SIZE - 4))
    yield lf.name
    lf.close()


def test_hash_large_file(large_file):
    hh = extraction.hash_large_file(large_file, TEST_CHUNK_SIZE)
    assert hh == "f03913edeb38a9569ccd6588b6338e58eb56fdcf0e8cecd0193cf68f180d6be1"


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


def dummy_long_task():
    time.sleep(10)
