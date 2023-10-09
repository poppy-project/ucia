from enum import Enum

class RobotState(Enum):
    API=0
    MODE=1

status: RobotState = RobotState.MODE

def set_status(new_status: RobotState):
    global status
    status = new_status