import logging


def createStandardLogger(_name=__name__, _filepath="slug.log"): 
    logger = logging.getLogger(_name)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s: %(funcName)s: %(message)s")

    file_handler = logging.FileHandler(_filepath) 
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(logging.StreamHandler())

    logger.info("\n--------------------------------------------- START LOGGING  ---------------------------------------------")
    logger.info("asctime: levelname: name: funcName: message")    
    return logger