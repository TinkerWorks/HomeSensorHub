#!/usr/bin/env python3

import coloredlogs
import logging
import verboselogs


def initialize_logger():

    dateformat = "%H:%M:%S"

    coloredlogs.install(level='INFO', milliseconds=True, datefmt=dateformat)

    fl_lg = logging.getLogger('filelock')
    fl_lg.setLevel('WARN')


def getLogger(name):
    logger = verboselogs.VerboseLogger(name)
    return logger


initialize_logger()
