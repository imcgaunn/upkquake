import os
import hashlib
import zipfile
import subprocess
import logging

import upkquake.constants as constants
import upkquake.util as util

from concurrent.futures import ThreadPoolExecutor


logging.basicConfig()
logger = logging.getLogger('upkquake-extraction')


def start_download_in_threadpool():
    # start downloading quake2 zip on a separate thread
    with ThreadPoolExecutor(max_workers=1) as executor:
        return executor.submit(download_q2_zip)


def download_q2_zip(url=constants.Q2_ARCHIVE_URL):
    try:
        util.download_file(url, constants.DEFAULT_ZIP_PATH)
    except Exception:
        logger.error('something went wrong downloading q2 zip.', exc_info=True)


def hash_large_file(file, chunksize):
    """ computes a sha256 digest of a large file by reading (at most) chunksize chunks
    at a time and feeding them to the hasher.
    """
    hasher = hashlib.sha256()
    with open(file, 'rb') as lf:
        chunk = lf.read(chunksize)
        while chunk:
            hasher.update(chunk)
            chunk = lf.read(chunksize)
    return hasher.hexdigest()


def verify_q2_zip(zip_path=constants.DEFAULT_ZIP_PATH):
    # TODO verify against sha256 hash in constants
    # read file in 8k chunks and update hasher in same increment
    if hash_large_file(zip_path, constants.HASH_CHUNK_SIZE) != constants.Q2_ARCHIVE_SHA256:
        raise Exception('bad zip file')


def _check_unpacked_files(unpacked_files):
    if not unpacked_files:
        raise Exception('files missing from the quake2 zip :(')
    try:
        unpacked_bin = [f for f in unpacked_files if f.endswith('.bin')][0]
    except IndexError:
        raise Exception('missing bin file in quake2 zip')
    try:
        unpacked_cue = [f for f in unpacked_files if f.endswith('.cue')][0]
    except IndexError:
        raise Exception('missing cue file in quake2 zip')
    return unpacked_bin, unpacked_cue


def unpack_cd_files(quake_zip_path):
    """ given path to quake2 zip file with bin/cue extract
        data and audio tracks with bchunk """
    util.mkdir_if_notexists(constants.CD_UNPACK_DIR)
    util.mkdir_if_notexists(os.path.join(constants.CD_UNPACK_DIR, 'music'))
    with zipfile.ZipFile(quake_zip_path) as qz:
        qz.extractall(path=constants.CD_UNPACK_DIR)
    unpacked_files = os.listdir(constants.CD_UNPACK_DIR)
    try:
        upkd_bin, upkd_cue = _check_unpacked_files(unpacked_files)
    except Exception:
        msg = 'something is wrong with the quake2 zip'
        logger.error(msg, exc_info=True)
        raise
    # the -s flag switches endianness of audio tracks. without it they
    # sound like static :(
    cmd = ['bchunk', '-s', upkd_bin, upkd_cue, 'Quake 2.iso']
    bchunk_result = subprocess.run(cmd,
                                   cwd=constants.CD_UNPACK_DIR,
                                   check=True)
    logger.info(f'bchunk result: {bchunk_result}')


def transform_cdr_name_to_ogg_name(cdr_track_name):
    iso_plus_idx = cdr_track_name.split('.')[1]
    idx_only = iso_plus_idx.strip('iso')
    music_dir = os.path.join(constants.CD_UNPACK_DIR, 'music')
    ogg_name = os.path.join(music_dir, f'{idx_only}.ogg')
    return ogg_name


def convert_with_sox(cdr_track_name):
    # on cmdline it would be sox $cdr_path $ogg_path and
    # the file extensions should be enough to tell it to convert
    ogg_name = transform_cdr_name_to_ogg_name(cdr_track_name)
    cmd = ['sox', cdr_track_name, ogg_name]
    sox_result = subprocess.run(cmd, check=True)
    logger.debug(f'sox conversion result: {sox_result}')


def convert_cdr_audio(cdr_dir):
    """ given a directory containing a bunch of cdr audio extracted
        from quake2 retail disk, convert all the tracks to ogg-vorbis
        with names expected by yamagi quake """
    cdr_files = [os.path.join(cdr_dir, f)
                 for f in os.listdir(cdr_dir) if f.endswith('.cdr')]
    try:
        for f in cdr_files:
            convert_with_sox(f)
    except subprocess.CalledProcessError:
        logger.error(f'failed to convert cdr to ogg :(', exc_info=True)
        raise
