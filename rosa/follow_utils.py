def look_and_follow(controller, target,
                    look_speed=0.15, asserv_p=0.4):
    if target is None:
        controller.set_speed('a', look_speed)
        controller.set_speed('b', look_speed)
    else:
        dx, _ = target

        def f(m, dx):
            dx = -dx if m == 'a' else dx
            return asserv_p * (0.5 * dx + 0.5)

        controller.set_speed('a', f('a', dx))
        controller.set_speed('b', -f('b', dx))
