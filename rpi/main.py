import logging

from manager.thymio.manager import ThymioManager

def run():
    manager = ThymioManager()
    while True:
        manager.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S')
    logger = logging.getLogger(__name__)

    run()
    