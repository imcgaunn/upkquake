import concurrent.futures
import pprint
import time

import pytest

import upkquake.extraction as extraction


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
