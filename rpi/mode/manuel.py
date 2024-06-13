from time import sleep

def set_speed(rosa, ls, rs):
    """Réglez la vitesse des roues gauche et droite."""
    rosa.left_wheel.speed = ls
    rosa.right_wheel.speed = rs

def stop(rosa):
    """Arrêtez le ROSA."""
    set_speed(rosa, 0, 0)

def forward(rosa, speed, duration=None):
    """Fait avancer le ROSA à la vitesse donnée pendant une durée donnée ou indéfiniment."""
    set_speed(rosa, speed, speed)
    if duration:
        sleep(duration)
        stop(rosa)

def backward(rosa, speed, duration=None):
    """Fait reculer le ROSA à la vitesse donnée pendant une durée donnée ou indéfiniment."""
    set_speed(rosa, -speed, -speed)
    if duration:
        sleep(duration)
        stop(rosa)

def turn_left(rosa, speed, duration=None):
    """Fait tourner le ROSA à gauche à la vitesse donnée pendant une durée donnée ou indéfiniment."""
    set_speed(rosa, speed, -speed)
    if duration:
        sleep(duration)
        stop(rosa)

def turn_right(rosa, speed, duration=None):
    """Fait tourner le ROSA à droite à la vitesse donnée pendant une durée donnée ou indéfiniment."""
    set_speed(rosa, -speed, speed)
    if duration:
        sleep(duration)
        stop(rosa)
        

def active_buzz(rosa, duration=1): 
    """Active le buzzer du ROSA pendant une durée donnée ou 1sec."""
    rosa.buzz(duration)

def active_led(rosa, led, state):
    """Met la led indiquéé à l'état indiquée """
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

def control(rosa, command, speed=None):
    """Contrôle le ROSA en fonction de la commande et de la vitesse donnée."""
    speed = max(min(speed, 1), 0)  # Assure que la vitesse est entre 0 et 1

    if command == 'forward':
        forward(rosa, speed)
    elif command == 'backward':
        backward(rosa, speed)
    elif command == 'left':
        turn_left(rosa, speed)
    elif command == 'right':
        turn_right(rosa, speed)
    elif command == 'stop':
        stop(rosa)
    elif command == "buzz":
        active_buzz(rosa)
    else:
        raise ValueError(f"Commande inconnue : {command}")
