import os
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


def test_hash_large_file(large_file):
    hh = util.hash_large_file(large_file, TEST_CHUNK_SIZE)
    assert hh == "f03913edeb38a9569ccd6588b6338e58eb56fdcf0e8cecd0193cf68f180d6be1"
