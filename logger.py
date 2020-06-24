import logging

def init_logger():
    logger = logging.getLogger("water_plants")
    logger.propagate = False 
    logger.setLevel(level=logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)-4s %(levelname)-8s %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(level=logging.DEBUG)
    ch.setFormatter(formatter)

    fh = logging.FileHandler('water_plant.log')
    fh.setLevel(level=logging.INFO)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)