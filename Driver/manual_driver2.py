from pynput.keyboard import Key, Listener
import sabertooth
import time
import threading

running = False

saber = sabertooth.Sabertooth()
def loading(key):
    while running:
        if (key == "w"):
            print("drive forward")
            saber.send_driving_command(100, 8)
            time.sleep(3)
        elif (key == "s"):
            print("drive backward")
            saber.send_driving_command(100, 9)
            time.sleep(3)
        elif (key == "a"):
            print("drive left")
            saber.send_driving_command(100, 10)
            time.sleep(3)
        elif (key == "d"):
            print("drive right")
            saber.send_driving_command(100, 11)
            time.sleep(3)



def on_press(key):
    global running
    if key.char == "w" or key.char == "s" or key.char == "a" or key.char == "d":
        running = True
        # create thread with function `loading`
        t = threading.Thread(target=loading, args = key.char)
        # start thread
        t.start()
    elif (key.char == "q"):
        running = False
        print("stop")
        saber.stop()


def on_release(key):
    global running
    print(key.char)
    if key.char == "w" or key.char == "s" or key.char == "a" or key.char == "d":
         running = False
         saber.stop()
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

