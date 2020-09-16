import functools
import logging
import os
import sys
import tempfile
import time
import shutil

import upkquake.constants as constants
import upkquake.extraction as extraction
import upkquake.util as util

from concurrent.futures import ThreadPoolExecutor


logging.basicConfig()
logger = logging.getLogger("upkquake-main")
logger.setLevel(logging.INFO)


def main(args=[]):
    # TODO: create a temporary directory to house all intermediate files/
    # to cache the dependencies from archive.org
    logger.info(f"creating {constants.CACHE_DIR_PATH} if necessary")
    util.mkdir_if_notexists(constants.CACHE_DIR_PATH)
    if not args:
        # before downloading, check if zip is already downloaded.
        # archive.org is slow and it's nice to have this cached
        already_downloaded = False
        try:
            if os.path.exists(constants.DEFAULT_ZIP_PATH):
                logger.info("quake2 zip found, checking integrity")
                # make sure this zip isn't corrupted
                extraction.verify_q2_zip(constants.DEFAULT_ZIP_PATH)
                already_downloaded = True
                logger.info("cached quake2 zip is valid, can skip dowload.")

        except Exception as e:
            logger.warn("the cached quake 2 zip appears to be corrupted :(")
            logger.warn("got exception from verify_q2_zip", exc_info=e)
            logger.warn("deleting and re-downloading from source")

        if not already_downloaded:
            logger.info("downloading quake2 zip from archive.org")
            logger.info(f"url: {constants.Q2_ARCHIVE_URL}")
            with ThreadPoolExecutor() as tpe:
                download_zip_to_cache = functools.partial(
                    extraction.download_q2_zip, output_dir=constants.CACHE_DIR_PATH
                )
                logger.info(f"starting download in separate threadpool")
                download_handle = tpe.submit(download_zip_to_cache)
                spinner = util.spinning_cursor()
                while download_handle.running():
                    # poor man's progress indicator...
                    # spins through a bunch of letters
                    # while the zip is still downloading.
                    sys.stdout.write(next(spinner))
                    sys.stdout.flush()
                    time.sleep(0.1)
                    sys.stdout.write("\b")
            # check the sha256 hash to determine if download completed successfully
            logger.info("checking integrity of downloaded quake2 zip")
            extraction.verify_q2_zip(zip_path=constants.DEFAULT_ZIP_PATH)
            logger.info("downloaded zip is valid!")
        logger.info(f"unpacking cd files to {constants.CD_UNPACK_DIR}")
        extraction.unpack_cd_files(
            constants.DEFAULT_ZIP_PATH, unpack_dir=constants.CD_UNPACK_DIR
        )
        logger.info(f"converting cdr audio to ogg")
        extraction.convert_cdr_audio(constants.CD_UNPACK_DIR)
        # TODO: move files around into the proper structure
        logger.info(f"preparation complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
