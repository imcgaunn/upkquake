import os


HERE = os.path.abspath(os.getcwd())

Q2_ARCHIVE_URL = "https://archive.org/download/QuakeII-CDImage/Quake II.zip"
Q2_ARCHIVE_SHA256 = "b05ae709287562e0d32354554f9d4861c5a0ac05b966b54d4c41898498e10545"

Q2_YAMAGI_PATCH_URL = "https://deponie.yamagi.org/quake2/idstuff/q2-3.20-x86-full-ctf.exe"  # TODO: find this URL
Q2_YAMAGI_PATCH_SHA256 = (
    "f82197c8c8089202a4b3a85d8833b0c2e827a709d205c760369407c212488baa"
)

HOME_DIR = os.getenv("USERPROFILE") if os.name == "nt" else os.getenv("HOME")
CACHE_DIR_PATH = os.path.join(HOME_DIR, ".cache", "upkquake")
DEFAULT_ZIP_PATH = os.path.join(CACHE_DIR_PATH, "Quake II.zip")
DEFAULT_PATCH_PATH = os.path.join(CACHE_DIR_PATH, "yamagi_patch.zip")
CD_UNPACK_DIR = os.path.join(CACHE_DIR_PATH, "unpacked_cd")

DOWNLOAD_CHUNK_BYTES = 1024
HASH_CHUNK_SIZE = 4096

PAKFILE_MD5S = {
    "baseq2/pak0.pak": "1ec55a724dc3109fd50dde71ab581d70",
    "baseq2/pak1.pak": "42663ea709b7cd3eb9b634b36cfecb1a",
    "baseq2/pak2.pak": "c8217cc5557b672a87fc210c2347d98d",
    "ctf/pak0.pak": "1f6bd3d4c08f7ed8c037b12fcffd2eb5",
    "rogue/pak0.pak": "5e2ecbe9287152a1e6e0d77b3f47dcb2",
    "xatrix/pak0.pak": "f5e7b04f7d6b9530c59c5e1daa873b51",
}
