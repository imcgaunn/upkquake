import logging
import os
import sys
import tempfile
import time

import upkquake.constants as constants
import upkquake.extraction as extraction
import upkquake.util as util

from concurrent.futures import ThreadPoolExecutor


logging.basicConfig()
logger = logging.getLogger('upkquake-main')


def main(args=[]):
    # TODO: create a temporary directory to house all intermediate files/
    # to cache the dependencies from archive.org
    cache_dir = os.path.join(os.getenv('HOME'), '.cache', 'upkquake')
    util.mkdir_if_notexists(cache_dir)
    if not args:
        # before downloading, check if zip is already downloaded.
        # archive.org is slow and it's nice to have this cached
        with ThreadPoolExecutor() as tpe:
            download_handle = tpe.submit(extraction.download_q2_zip)
            spinner = util.spinning_cursor()
            while download_handle.running():
                # poor man's progress indicator...
                # spins through a bunch of letters
                # while the zip is still downloading.
                sys.stdout.write(next(spinner))
                sys.stdout.flush()
                time.sleep(0.1)
                sys.stdout.write('\b')
        # check the sha256 hash to determine if download completed successfully
        extraction.verify_q2_zip(zip_path=constants.DEFAULT_ZIP_PATH)
        extraction.unpack_cd_files(constants.DEFAULT_ZIP_PATH)
        extraction.convert_cdr_audio(constants.CD_UNPACK_DIR)
    return 0


if __name__ == '__main__':
    sys.exit(main())

