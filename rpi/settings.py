from enum import Enum

class RobotState(Enum):
    API=0
    MODE=1

status: RobotState = RobotState.MODE

loading_model = True

def set_status(new_status: RobotState):
    global status
    status = new_status