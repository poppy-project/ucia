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
         
def active_buzz(duration=1):
    """Active le buzzer du ROSA pendant une durée donnée ou 1sec."""
    global rosa
    define_rosa()
    rosa.buzz(duration)

def active_led(led, color, duration=2):
    """Met la led indiquée à l'état indiqué"""
    global rosa
    define_rosa()
    duration = max(duration, 2)

    colors = {
        "off": [0, 0, 0],
        "red": [32, 0, 0],
        "green": [0, 32, 0],
        "blue": [0, 0, 32],
        "yellow": [32, 32, 0],
        "purple": [32, 0, 32],
        "cyan": [0, 32, 32],
        "white": [32, 32, 32]
    }
    
    if color in colors:
        color_value = colors[color]
        
        if led == "left":
            rosa.leds.bottom.left.color = color_value
        elif led == "right":
            rosa.leds.bottom.right.color = color_value
        elif led == "both":
            rosa.leds.bottom.right.color = color_value
            rosa.leds.bottom.left.color = color_value
        sleep(duration)

    else:
        print(f"Couleur {color} non reconnue. Utilisez une des couleurs suivantes : {', '.join(colors.keys())}.")


def get_ground_value(sensor):
    """renvoit la valeur du capteur de sol indiqué"""
    global rosa
    define_rosa()
    reflected = rosa.ground_reflected
    if sensor == "left":
        print(f"valeur du capteur gauche : {reflected[0]}")
        return reflected[0]
    elif sensor == "right":
        print(f"valeur du capteur droit : {reflected[1]}")
        return reflected[1]
    else :
        return (f"{sensor} non reconnue.")
    
    
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
