import logging
import sys
import time

import upkquake.constants as constants
import upkquake.extraction as extraction
import upkquake.util as util

from concurrent.futures import ThreadPoolExecutor


logging.basicConfig()
logger = logging.getLogger('upkquake-main')


def main(args=[]):
    if not args:
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
        download_completed = download_handle.result()
        if not download_completed:
            msg = 'failed to download quake II.zip :('
            raise Exception(msg)
        extraction.unpack_cd_files(constants.DEFAULT_ZIP_PATH)
        extraction.convert_cdr_audio(constants.CD_UNPACK_DIR)
    return 0


if __name__ == '__main__':
    sys.exit(main())
