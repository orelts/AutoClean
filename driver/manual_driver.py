from inputs import get_gamepad
import sabertooth
import time

## this file exists for driving demo. using xbox controller to navigate
## (important) activate controller before activating the TX2
## to activate manual driving mode press 3 times on Right-Back button on xbox controller
## to deactivate this mode press 3 times on Left-Back button on xbox controller


manual_driving_mode = 'OFF'
startup_RB_count = 0
end_time = time.time() + 30


while time.time() < end_time and manual_driving_mode == 'OFF':
    try:
        events = get_gamepad()
    except Exception:
        break
    for event in events:
        print (event.code,event.state)
        if (event.code == 'BTN_TR' and event.state == 1):
            startup_RB_count = startup_RB_count +1
        if startup_RB_count == 3:
            manual_driving_mode = 'ON'
            break


if manual_driving_mode == 'ON':
    saber = sabertooth.sabertooth()
    while manual_driving_mode == 'ON':
        try:
            events = get_gamepad()
        except Exception:
            break
        for event in events:
            print(event.code, event.state)
            ##stopping sequence
            if (event.code == 'BTN_TL' and event.state == 1):
                startup_RB_count = startup_RB_count - 1
            if startup_RB_count == 0:
                manual_driving_mode = 'OFF'

            elif event.code != 'BTN_TL':
                if (event.code == 'ABS_HAT0Y' and event.state == -1):
                    saber.drive_forward(50)
                if (event.code == 'ABS_HAT0Y' and event.state == 1):
                    saber.drive_backwards(50)
                if (event.code == 'ABS_HAT0X' and event.state == -1):
                    saber.turn_left(50)
                if (event.code == 'ABS_HAT0X' and event.state == 1):
                    saber.turn_right(50)
