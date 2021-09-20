import logging
import sys

import upkquake.assets as assets
import upkquake.constants as constants
import upkquake.extraction as extraction
import upkquake.util as util
import os.path

from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO, handlers=[RichHandler()])
logger = logging.getLogger("upkquake-main")
logger.setLevel(logging.INFO)


def main(args=[]):
    logger.info(f"creating {constants.CACHE_DIR_PATH} if necessary")
    util.mkdir_if_notexists(constants.CACHE_DIR_PATH)

    logger.info("downloading assets: ")
    for a in assets.ALL:
        logger.info(f"downloading {a['url']} to {a['output_path']}")
        assets.download_with_cache(a)
    logger.info(f"unpacking zip and splitting cd data/audio tracks")
    data_track, cdr_files = extraction.unpack_zip_and_split_cd_tracks(
        constants.DEFAULT_ZIP_PATH, constants.CD_UNPACK_DIR
    )
    logger.debug(f"got data track: {data_track}")
    logger.debug(f"got cdr_files: {cdr_files}")
    logger.info("converting cdr audio to ogg")
    for cdrf in cdr_files:
        extraction.convert_with_sox(os.path.join(constants.CD_UNPACK_DIR, cdrf))
    # TODO: move files around into the proper structure
    logger.info("preparation complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
