import os
import hashlib
import zipfile
import subprocess
import logging
import shutil

import upkquake.constants as constants
import upkquake.util as util


logging.basicConfig()
logger = logging.getLogger("upkquake-extraction")
logger.setLevel("DEBUG")


def download_q2_zip(url=constants.Q2_ARCHIVE_URL):
    try:
        util.download_file(url, constants.DEFAULT_ZIP_PATH)
    except Exception:
        logger.error("something went wrong downloading q2 zip.", exc_info=True)


def hash_large_file(file, chunksize):
    """computes a sha256 digest of a large file by reading (at most) chunksize
    chunks at a time and feeding them to the hasher.
    """
    hasher = hashlib.sha256()
    with open(file, "rb") as lf:
        chunk = lf.read(chunksize)
        while chunk:
            hasher.update(chunk)
            chunk = lf.read(chunksize)
    return hasher.hexdigest()


def verify_q2_zip(zip_path=constants.DEFAULT_ZIP_PATH):
    hash = hash_large_file(zip_path, constants.HASH_CHUNK_SIZE)
    if hash != constants.Q2_ARCHIVE_SHA256:
        raise Exception("bad zip file")


def _check_unpacked_files(unpacked_files):
    if not unpacked_files:
        raise Exception("files missing from the quake2 zip :(")
    try:
        unpacked_bin = [f for f in unpacked_files if f.endswith(".bin")][0]
    except IndexError:
        raise Exception("missing bin file in quake2 zip")
    try:
        unpacked_cue = [f for f in unpacked_files if f.endswith(".cue")][0]
    except IndexError:
        raise Exception("missing cue file in quake2 zip")
    return unpacked_bin, unpacked_cue


def unpack_cd_files(quake_zip_path, unpack_dir=constants.CD_UNPACK_DIR):
    """given path to quake2 zip file with bin/cue extract
    data and audio tracks with bchunk"""
    util.mkdir_if_notexists(unpack_dir)
    util.mkdir_if_notexists(os.path.join(unpack_dir, "music"))
    with zipfile.ZipFile(quake_zip_path) as qz:
        qz.extractall(path=unpack_dir)
    unpacked_files = os.listdir(unpack_dir)
    try:
        upkd_bin, upkd_cue = _check_unpacked_files(unpacked_files)
    except Exception:
        msg = "something is wrong with the quake2 zip"
        logger.error(msg, exc_info=True)
        raise
    # the -s flag switches endianness of audio tracks. without it they
    # sound like static :(
    cmd = ["bchunk", "-s", upkd_bin, upkd_cue, "Quake 2.iso"]
    bchunk_result = subprocess.run(cmd, cwd=unpack_dir, check=True)
    logger.info(f"bchunk result: {bchunk_result}")


def extract_gamefiles_from_iso(isopath, output_dir):
    # pull Install/Data/baseq2 from iso and cleanup extra files
    baseq2_relpath = "Install/Data/baseq2"
    cmd = [
        "7z",
        "x",
        "-tiso",
        f"{isopath}",
        f"{baseq2_relpath}",
        f"-o{output_dir}",
        "-y",
    ]
    extract_result = subprocess.run(cmd, check=True)
    logger.info(f"7z extract result: {extract_result}")
    # TODO: remove unnecessary files (optional).
    # considering this optional because they don't take up much space at all
    # this game was released in 1997...
    baseq2_extracted = os.path.join(f"{output_dir}", baseq2_relpath)
    shutil.move(baseq2_extracted, f"{output_dir}/baseq2")
    shutil.rmtree(f"{output_dir}/Install")
    logger.info(f"cleaned up {output_dir}/Install")


def extract_gamefiles_from_yamagi_patch(patch_exe_path, output_dir):
    cmd = ["7z", "x", f"{patch_exe_path}", "*", f"-o{output_dir}", "-y"]
    extract_result = subprocess.run(cmd, check=True)
    logger.info(f"7z extract result: {extract_result}")


def cdr_name_to_ogg_name(cdr_track_name, output_dir=constants.CD_UNPACK_DIR):
    iso_plus_idx = cdr_track_name.split(".")[1]
    idx_only = iso_plus_idx.strip("iso")
    music_dir = os.path.join(output_dir, "music")
    ogg_name = os.path.join(music_dir, f"{idx_only}.ogg")
    return ogg_name


def convert_with_sox(cdr_path):
    # on cmdline it would be sox $cdr_path $ogg_path and
    # the file extensions should be enough to tell it to convert
    ogg_name = cdr_name_to_ogg_name(cdr_path)
    cmd = ["sox", cdr_path, ogg_name]
    sox_result = subprocess.run(cmd, check=True)
    logger.debug(f"sox conversion result: {sox_result}")


def convert_cdr_audio(cdr_dir):
    """given a directory containing a bunch of cdr audio extracted
    from quake2 retail disk, convert all the tracks to ogg-vorbis
    with names expected by yamagi quake"""
    cdr_files = [
        os.path.join(cdr_dir, f) for f in os.listdir(cdr_dir) if f.endswith(".cdr")
    ]
    try:
        for f in cdr_files:
            convert_with_sox(f)
    except subprocess.CalledProcessError:
        logger.error(f"failed to convert cdr to ogg :(", exc_info=True)
        raise
