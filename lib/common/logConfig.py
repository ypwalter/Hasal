import os
import logging


def get_logger(name, enable_advance=None):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if enable_advance:
        logger.setLevel(logging.DEBUG)
        return logger
    else:
        if os.getenv("ENABLE_ADVANCE"):
            if int(os.getenv("ENABLE_ADVANCE")) == 1:
                logger.setLevel(logging.DEBUG)
                return logger
    logger.setLevel(logging.INFO)
    return logger
