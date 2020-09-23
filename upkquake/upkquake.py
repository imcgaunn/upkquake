import logging
import sys

import upkquake.constants as constants
import upkquake.extraction as extraction
import upkquake.util as util

logging.basicConfig()
logger = logging.getLogger("upkquake-main")
logger.setLevel(logging.INFO)


def main(args=[]):
    logger.info(f"creating {constants.CACHE_DIR_PATH} if necessary")
    util.mkdir_if_notexists(constants.CACHE_DIR_PATH)
    # before downloading, check if zip is already downloaded.
    # archive.org is slow and it's nice to have this cached

    # TODO: download assets

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
