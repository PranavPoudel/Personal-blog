import logging
import sys

def setup_logger():
    logger = logging.getLogger("blog_logger")
    logger.setLevel(logging.DEBUG)

    #create a handler to output to the console
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    #formatting the log message
    formatter = logging.Formatter("%(asctme)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

logger = setup_logger()

