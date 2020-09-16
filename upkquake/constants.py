import os


HERE = os.path.abspath(os.getcwd())
Q2_ARCHIVE_URL = "https://archive.org/download/QuakeII-CDImage/Quake II.zip"
Q2_ARCHIVE_SHA256 = "b05ae709287562e0d32354554f9d4861c5a0ac05b966b54d4c41898498e10545"
Q2_YAMAGI_PATCH_URL = ""  # TODO: find this URL
CACHE_DIR_PATH = os.path.join(os.getenv("HOME"), ".cache", "upkquake")
DEFAULT_ZIP_PATH = os.path.join(CACHE_DIR_PATH, "Quake II.zip")
CD_UNPACK_DIR = os.path.join(CACHE_DIR_PATH, "unpacked_cd")

DOWNLOAD_CHUNK_BYTES = 1024
HASH_CHUNK_SIZE = 4096
