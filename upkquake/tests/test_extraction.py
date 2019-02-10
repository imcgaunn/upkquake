import pytest
import tempfile
import upkquake.extraction as extraction


TEST_CHUNK_SIZE = 4096


@pytest.fixture()
def large_file():
    lf = tempfile.NamedTemporaryFile()
    for i in range(10000):
        lf.write(b'0x42' * (TEST_CHUNK_SIZE - 4))
    yield lf.name
    lf.close()


def test_hash_large_file(large_file):
    hh = extraction.hash_large_file(large_file, TEST_CHUNK_SIZE)
    assert hh == 'f03913edeb38a9569ccd6588b6338e58eb56fdcf0e8cecd0193cf68f180d6be1'
