#!/usr/bin/python
import time
import daemon
import lockfile
import logging

logger = logging.getLogger('display')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('display.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

context = daemon.DaemonContext(
        pidfile=lockfile.FileLock('./display.pid'),
        working_directory=".",
        files_preserve=[fh.stream])

with context:
    try:
        from timestamp_display import Display
        logger.info("Starting the display")
        dis = Display(".")
        dis.fill()
        logger.info("Stopped Display")

    except Exception as e:
        logger.error(f"Display process had issues {e}")

