from time import sleep
from rosa import Rosa

# Définition de la variable globale
rosa = None

def define_rosa():
    global rosa
    if rosa is None:
        rosa = Rosa('rosa.local', local_robot=False)  # Initialisez Rosa correctement
    return rosa

def set_speed(ls, rs):
    """Réglez la vitesse des roues gauche et droite."""
    global rosa
    define_rosa()    
    speedls = max(min(ls, 1), 0)  # Assure que la vitesse est entre 0 et 1
    speedrs = max(min(rs, 1), 0)  # Assure que la vitesse est entre 0 et 1

    rosa.left_wheel.speed = speedls
    rosa.right_wheel.speed = speedrs

def stop():
    """Arrêtez le ROSA."""
    set_speed(0, 0)

def forward(speed, duration=None):
    """Fait avancer le ROSA à la vitesse donnée pendant une durée donnée ou indéfiniment."""
    set_speed(speed, speed)
    if duration:
        sleep(duration)
        stop()

def backward(speed, duration=None):
    """Fait reculer le ROSA à la vitesse donnée pendant une durée donnée ou indéfiniment."""
    set_speed(-speed, -speed)
    if duration:
        sleep(duration)
        stop()

def turn_left(speed, duration=None):
    """Fait tourner le ROSA à gauche à la vitesse donnée pendant une durée donnée ou indéfiniment."""
    set_speed(speed, -speed)
    if duration:
        sleep(duration)
        stop()

def turn_right(speed, duration=None):
    """Fait tourner le ROSA à droite à la vitesse donnée pendant une durée donnée ou indéfiniment."""
    set_speed(-speed, speed)
    if duration:
        sleep(duration)
        stop()
        
def get_distance():
    global rosa
    define_rosa() 
    return(rosa.get_front_distances())
    
def get_ground_distance():
    global rosa
    define_rosa() 
    return sum(rosa.get_distance('ground-front-left'), rosa.get_distance('ground-front-right')) /2

def active_buzz(duration=1):
    """Active le buzzer du ROSA pendant une durée donnée ou 1sec."""
    global rosa
    define_rosa()
    rosa.buzz(duration)

def active_led(led, state):
    """Met la led indiquée à l'état indiqué"""
    global rosa
    define_rosa()
    if led == "left":
        if state == "on":
            rosa.left_led.on()
        elif state == "off":
            rosa.left_led.off()
    elif led == "right":
        if state == "on":
            rosa.right_led.on()
        elif state == "off":
            rosa.right_led.off()

def control(command, speed=None):
    """Contrôle le ROSA en fonction de la commande et de la vitesse donnée."""
    global rosa
    define_rosa()

    if command == 'forward':
        forward(speed)
    elif command == 'backward':
        backward(speed)
    elif command == 'left':
        turn_left(speed)
    elif command == 'right':
        turn_right(speed)
    elif command == 'stop':
        stop()
    elif command == "buzz":
        active_buzz()
    else:
        raise ValueError(f"Commande inconnue : {command}")
