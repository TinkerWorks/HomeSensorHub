#!/usr/bin/env python3

import coloredlogs
import verboselogs


def initialize_logger():

    dateformat = "%H:%M:%S"

    coloredlogs.install(level='SPAM', milliseconds=True, datefmt=dateformat)


def getLogger(name):
    logger = verboselogs.VerboseLogger(name)
    return logger


initialize_logger()
