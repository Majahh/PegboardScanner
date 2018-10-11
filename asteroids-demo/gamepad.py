import threading
from evdev import InputDevice, categorize, ecodes

aCode = 0
bCode = 1
xCode = 2
yCode = 3
lCode = 4
rCode = 5
selectCode = 6
startCode = 7
leftCode = 8
rightCode = 9
upCode = 10
downCode = 11

class GamePad(threading.Thread):
    def __init__(self, device_path):
        threading.Thread.__init__(self)
        self.gamepad = InputDevice(device_path)
        self.buttons = [False] * 12

    def run(self):
        aBtn = 289
        bBtn = 290
        xBtn = 288
        yBtn = 291
        lBtn = 292
        rBtn = 294
        selBtn = 296
        staBtn = 297

        for event in self.gamepad.read_loop():
            if event.type == ecodes.EV_KEY:
                if event.value == 1:
                    if event.code == xBtn:
                        self.buttons[xCode] = True
                    elif event.code == bBtn:
                        self.buttons[bCode] = True
                    elif event.code == aBtn:
                        self.buttons[aCode] = True
                    elif event.code == yBtn:
                        self.buttons[yCode] = True
                    elif event.code == lBtn:
                        self.buttons[lCode] = True
                    elif event.code == rBtn:
                        self.buttons[rCode] = True
                    elif event.code == selBtn:
                        self.buttons[selectCode] = True
                    elif event.code == staBtn:
                        self.buttons[startCode] = True
                elif event.value == 0:
                    if event.code == xBtn:
                        self.buttons[xCode] = False
                    elif event.code == bBtn:
                        self.buttons[bCode] = False
                    elif event.code == aBtn:
                        self.buttons[aCode] = False
                    elif event.code == yBtn:
                        self.buttons[yCode] = False
                    elif event.code == lBtn:
                        self.buttons[lCode] = False
                    elif event.code == rBtn:
                        self.buttons[rCode] = False
                    elif event.code == selBtn:
                        self.buttons[selectCode] = False
                    elif event.code == staBtn:
                        self.buttons[startCode] = False

            # Analog gamepad
            elif event.type == ecodes.EV_ABS:
                absevent = categorize(event)
                if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_X":
                     if absevent.event.value == 0:
                         self.buttons[leftCode] = True
                     elif absevent.event.value == 255:
                         self.buttons[rightCode] = True
                     elif absevent.event.value == 127:
                         self.buttons[leftCode] = False
                         self.buttons[rightCode] = False
                         self.buttons[upCode] = False
                         self.buttons[downCode] = False
                elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_Y":
                     if absevent.event.value == 0:
                         self.buttons[upCode] = True
                     elif absevent.event.value == 255:
                         self.buttons[downCode] = True
                     elif absevent.event.value == 127:
                         self.buttons[leftCode] = False
                         self.buttons[rightCode] = False
                         self.buttons[upCode] = False
                         self.buttons[downCode] = False

# When running GamePad module as main, just print out the state of the
# buttons array
if __name__ == "__main__":
    gamepad = GamePad()
    gamepad.setDaemon(True)
    gamepad.start()

    while True:
        print(gamepad.buttons)
