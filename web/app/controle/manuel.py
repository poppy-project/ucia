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
    speedls = max(min(ls, 1), -1)  # Assure que la vitesse est entre 0 et 1
    speedrs = max(min(rs, 1), -1)  # Assure que la vitesse est entre 0 et 1

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
    set_speed(-speed, speed)
    if duration:
        sleep(duration)
        stop()

def turn_right(speed, duration=None):
    """Fait tourner le ROSA à droite à la vitesse donnée pendant une durée donnée ou indéfiniment."""
    set_speed(speed, -speed)
    if duration:
        sleep(duration)
        stop()
         
def active_led(led, color, duration=2):
    """Met la led indiquée à l'état indiqué"""
    global rosa
    define_rosa()
    duration = max(duration, 2)

    colors = {
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
        return reflected[0]
    elif sensor == "right":
        return reflected[1]
    else :
        return (f"{sensor} non reconnue.")
    
def get_distance_value(sensor):
    """renvoit la valeur des capteurs avant"""
    global rosa
    define_rosa()
    reflected = rosa.prox_horizontal[sensor]
    return reflected
   
def play_note(hertz, ds):
    """Joue une seule note."""
    global rosa
    define_rosa()
    ds *= 100
    rosa.sound.frequency(hertz, ds)

def play_notes(notes):
    """Joue une série de notes."""
    for hertz, ds in notes:
        if hertz == 0 :
            sleep(ds)
        else :
            play_note(hertz, ds)
            sleep(ds)

def make_musique(song):
    """Joue une mélodie définie."""
    global rosa
    define_rosa()
    
    melodies = {
    "twinkle_twinkle": [
        [392, 0.5], [392, 0.5], [587, 0.5], [587, 0.5], [659, 0.5], [659, 0.5], [587, 1], 
        [523, 0.5], [523, 0.5], [494, 0.5], [494, 0.5], [440, 0.5], [440, 0.5], [392, 1],
        [587, 0.5], [587, 0.5], [523, 0.5], [523, 0.5], [494, 0.5], [494, 0.5], [440, 1], 
        [587, 0.5], [587, 0.5], [523, 0.5], [523, 0.5], [494, 0.5], [494, 0.5], [440, 1]
    ],
    "frere_jacques": [
        [261, 0.5], [294, 0.5], [330, 0.5], [261, 0.5], 
        [261, 0.5], [294, 0.5], [330, 0.5], [261, 0.5], 
        [330, 0.5], [349, 0.5], [392, 0.5], 
        [330, 0.5], [349, 0.5], [392, 0.5], 
        [392, 0.25], [440, 0.25], [392, 0.25], [349, 0.25], [330, 0.5], [261, 0.5], 
        [392, 0.25], [440, 0.25], [392, 0.25], [349, 0.25], [330, 0.5], [261, 0.5],
        [261, 0.5], [392, 0.5], [261, 0.5]
    ],
    "joyeux_anniversaire": [
        [264, 0.25], [264, 0.25], [297, 0.5], [264, 0.5], [352, 0.5], [330, 1.0],
        [264, 0.25], [264, 0.25], [297, 0.5], [264, 0.5], [396, 0.5], [352, 1.0],
        [264, 0.25], [264, 0.25], [528, 0.5], [440, 0.5], [352, 0.5], [330, 0.5], [297, 1.0],
        [466, 0.25], [466, 0.25], [440, 0.5], [352, 0.5], [396, 0.5], [352, 1.0]
    ],
    "super_mario": [
        [659, 0.03125], [659, 0.03125], [0, 0.03125], [659, 0.03125], [0, 0.03125], [523, 0.03125], [659, 0.03125], [784, 0.03125], [0, 0.09375], [392, 0.03125],
        [0, 0.09375], [523, 0.03125], [0, 0.0625], [392, 0.03125], [0, 0.0625], [330, 0.03125], [0, 0.0625], [440, 0.03125], [0, 0.03125], [494, 0.03125],
        [0, 0.03125], [466, 0.03125], [0, 0.0105], [440, 0.03125], [0, 0.03125], [392, 0.03125], [659, 0.03125], [784, 0.03125], [880, 0.03125], [0, 0.03125],
        [698, 0.03125], [784, 0.03125], [0, 0.03125], [659, 0.03125], [0, 0.03125], [523, 0.03125], [587, 0.03125], [494, 0.03125], [0, 0.03125],
        [523, 0.03125], [0, 0.0625], [392, 0.03125], [0, 0.0625], [330, 0.03125], [0, 0.0625], [440, 0.03125], [0, 0.03125], [494, 0.03125], [0, 0.03125],
        [466, 0.03125], [0, 0.0105], [440, 0.03125], [0, 0.03125], [392, 0.03125], [659, 0.03125], [784, 0.03125], [880, 0.03125], [0, 0.03125],
        [698, 0.03125], [784, 0.03125], [0, 0.03125], [659, 0.03125], [0, 0.03125], [523, 0.03125], [587, 0.03125], [494, 0.03125]
    ],
}
    
    if song in melodies:
        play_notes(melodies[song])
    else:
        print(f"Mélodie '{song}' non trouvée.")
    
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
    else:
        raise ValueError(f"Commande inconnue : {command}")
