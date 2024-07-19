import logging
import logging.config

def setup_logger(name):
    logging.config.fileConfig('config/logging.conf')
    return logging.getLogger(name)