import pytest


@pytest.fixture(scope="function")
def mock_file_server():
    pass


@pytest.fixture(scope="function")
def test_asset_infos():
    asset_infos = [
        {
            "url": "http://localhost:8888/test_asset_one.dat",
            "checksum": "",
            "output_path": "",
        },
        {
            "url": "http://localhost:8888/test_asset_two.dat",
            "checksum": "",
            "output_path": "",
        },
        {
            "url": "http://localhost:8888/test_asset_two.dat",
            "checksum": "",
            "output_path": "",
        },
    ]
    return asset_infos
