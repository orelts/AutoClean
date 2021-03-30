from keyboard_master import keyboard
import sabertooth
import time

if __name__ == '__main__':
    manual_driving_mode = 'OFF'
    end_time = time.time() + 60


    #entering manual driving mode by pressing enter, exiting by pressing escape
    while(manual_driving_mode == 'OFF' and time.time() < end_time):
        if keyboard.is_pressed('enter'):
                manual_driving_mode = 'ON'

    while (manual_driving_mode == 'ON'):
        saber = sabertooth.sabertooth()
        if keyboard.is_pressed('esc'):
            manual_driving_mode = 'OFF'
            saber.stop()
        elif keyboard.is_pressed('up'):
            print('fwd')
            saber.drive_forward(50)
            time.sleep(0.5)
        elif keyboard.is_pressed('down'):
            print('back')
            saber.drive_backwards(50)
            time.sleep(0.5)
        elif keyboard.is_pressed('right'):
            print('right')
            saber.turn_right(50)
            time.sleep(0.5)
        elif keyboard.is_pressed('left'):
            print('left')
            saber.turn_left(50)
            time.sleep(0.5)
        elif keyboard.is_pressed('space'):
            print('stop')
            saber.stop()
            time.sleep(0.5)


    exit()



## xbox controller,  currently working only on windows
## this file exists for driving demo. using xbox controller to navigate
## (important) activate controller before activating the TX2
## to activate manual driving mode press 3 times on Right-Back button on xbox controller
## to deactivate this mode press 3 times on Left-Back button on xbox controller

#     while time.time() < end_time and manual_driving_mode == 'OFF':
#         try:
#             events = get_key()
#         except Exception:
#             break
#         for event in events:
#             print (event.code,event.state)
#             if (event.code == 'BTN_TR' and event.state == 1):
#                 startup_RB_count = startup_RB_count +1
#             if startup_RB_count == 3:
#                 manual_driving_mode = 'ON'
#                 break
#
#
#     if manual_driving_mode == 'ON':
#         saber = sabertooth.sabertooth()
#         while manual_driving_mode == 'ON':
#             try:
#                 events = get_key()
#             except Exception:
#                 break
#             for event in events:
#                 print(event.code, event.state)
#                 ##stopping sequence
#                 if (event.code == 'BTN_TL' and event.state == 1):
#                     startup_RB_count = startup_RB_count - 1
#                 if startup_RB_count == 0:
#                     manual_driving_mode = 'OFF'
#
#                 elif event.code != 'BTN_TL':
#                     if (event.code == 'ABS_HAT0Y' and event.state == -1):
#                         saber.drive_forward(50)
#                     if (event.code == 'ABS_HAT0Y' and event.state == 1):
#                         saber.drive_backwards(50)
#                     if (event.code == 'ABS_HAT0X' and event.state == -1):
#                         saber.turn_left(50)
#                     if (event.code == 'ABS_HAT0X' and event.state == 1):
#                         saber.turn_right(50)
#