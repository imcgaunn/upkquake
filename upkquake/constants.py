import os


HERE = os.path.abspath(os.getcwd())
Q2_ARCHIVE_URL = 'https://archive.org/download/QuakeII-CDImage/Quake II.zip'
Q2_ARCHIVE_SHA256 = 'b05ae709287562e0d32354554f9d4861c5a0ac05b966b54d4c41898498e10545'
DEFAULT_ZIP_PATH = os.path.join(HERE, 'Quake II.zip')
CD_UNPACK_DIR = os.path.join(HERE, 'unpacked_cd')

DOWNLOAD_CHUNK_BYTES = 1024
HASH_CHUNK_SIZE = 4096
