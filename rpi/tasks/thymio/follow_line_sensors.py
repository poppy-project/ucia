import logging
from tasks.base import Task
from controller.thymio.controller import ThymioController

class FollowLineSensors(Task):
    def __init__(self, controller: ThymioController):
        self.controller = controller
        self.logger = logging.getLogger(__name__)
        self.init()
    
    def init(self):
        self.controller.set_led("top", [0, 0, 16])
  
    def run(self):
        self.logger.info("FOLLOW LINE")

        reflected = self.controller.get_state("prox.ground.reflected")

        # Seuil de détection entre noir et blanc. 
        # Une valeur médiane entre 200 (noir) et 800 (blanc) pourrait être 500.
        threshold = 400
        # return
        if reflected[0] > threshold and reflected[1] < threshold:
            print("right")
            self.controller.set_speed(0, 0.1)
        elif reflected[0] < threshold and reflected[1] > threshold:
            print("left")
            self.controller.set_speed(0.1, 0)
        elif reflected[0] < threshold and reflected[1] < threshold:
            print("straigh")
            self.controller.set_speed(0.1, 0.1)
        else:  # Les deux capteurs sont sur fond blanc, perte de la ligne.
            print("lost")
            # Ici, vous pouvez soit arrêter Thymio, soit lui faire faire une autre action pour retrouver la ligne.
            self.controller.set_speed(0.0, 0.0)

        print(reflected)

    def close(self):
        pass