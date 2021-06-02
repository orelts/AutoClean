import keyboard
import sabertooth
import time
import pynput as pyn

from crane import lynxmotion

## manual
## entering manual driving mode by pressing 'enter', exiting by pressing 'escape'
## arrows control the direction of movement
## WASD control the crane

if __name__ == '__main__':
    manual_driving_mode = 'OFF'
    end_time = time.time() + 60
    saber = sabertooth.Sabertooth()
    saber.drive_forward(50, 5)
    saber.stop()
    # while(manual_driving_mode == 'OFF' and time.time() < end_time):
    #     if keyboard.is_pressed('enter'):
    #         manual_driving_mode = 'ON'
    #         saber = sabertooth.Sabertooth()
    #         # lynx = lynxmotion()
    # while (manual_driving_mode == 'ON'):
    #     if keyboard.is_pressed('esc'):
    #         manual_driving_mode = 'OFF'
    #         saber.stop()
    #     elif keyboard.is_pressed('up'):
    #         print('fwd')
    #         saber.drive_forward(50)
    #     elif keyboard.is_pressed('down'):
    #         print('back')
    #         saber.drive_backwards(50)
    #     elif keyboard.is_pressed('right'):
    #         print('right')
    #         saber.turn_right(50)
    #     elif keyboard.is_pressed('left'):
    #         print('left')
    #         saber.turn_left(50)
    #     elif keyboard.is_pressed('space'):
    #         print('stop')
    #         saber.stop()
    # exit()
