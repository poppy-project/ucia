def set_led_color(rosa, color):
    """Set LED color based on the robot's current state."""
    if color == 'blue':
        rosa.leds.bottom.left.color = [0, 0, 32] 
        rosa.leds.bottom.right.color = [0, 0, 32]
    elif color == 'purple':
        rosa.leds.bottom.left.color = [16, 0, 16] 
        rosa.leds.bottom.right.color = [16, 0, 16]
    elif color == 'green':
        rosa.leds.bottom.left.color = [0, 32, 0]
        rosa.leds.bottom.right.color = [0, 32, 0]
    elif color == 'yellow':
        rosa.leds.bottom.left.color = [32, 32, 0]
        rosa.leds.bottom.right.color = [32, 32, 0]