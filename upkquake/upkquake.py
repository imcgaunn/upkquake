import logging
import sys
import time

import upkquake.constants as constants
import upkquake.extraction as extraction


logging.basicConfig()
logger = logging.getLogger('upkquake-main')


def main(args=[]):
    if not args:
        download_handle = extraction.start_download_in_threadpool()
        while download_handle.running():
            print('still downloadin...')
            time.sleep(10)
        download_completed = download_handle.result()
        if not download_completed:
            msg = 'failed to download quake II.zip :('
            raise Exception(msg)
        extraction.unpack_cd_files(constants.DEFAULT_ZIP_PATH)
        extraction.convert_cdr_audio(constants.CD_UNPACK_DIR)
    return 0


if __name__ == '__main__':
    sys.exit(main())
