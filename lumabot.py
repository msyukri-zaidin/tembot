import ctypes
from ctypes import wintypes
import time
import pyautogui
import keyboard
import random

encounter = 0
zeph = 0

user32 = ctypes.WinDLL('user32', use_last_error=True)
LEAVE = False
REFRESH = False
JUST_REFRESHED = False

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008

MAPVK_VK_TO_VSC = 0

# msdn.microsoft.com/en-us/library/dd375731
VK_TAB = 0x09
VK_MENU = 0x12

# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg", wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))


class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))

    _anonymous_ = ("_input",)
    _fields_ = (("type", wintypes.DWORD),
                ("_input", _INPUT))


LPINPUT = ctypes.POINTER(INPUT)


def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args


user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT,  # nInputs
                             LPINPUT,  # pInputs
                             ctypes.c_int)  # cbSize


# Functions

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def AltTab():
    """Press Alt+Tab and hold Alt key for 2 seconds
    in order to see the overlay.
    """
    PressKey(VK_MENU)  # Alt
    PressKey(VK_TAB)  # Tab
    ReleaseKey(VK_TAB)  # Tab~
    time.sleep(2)
    ReleaseKey(VK_MENU)  # Alt~


def on_press(key):
    print('{0} pressed'.format(
        key))


def on_release(key):
    print('{0} release'.format(
        key))

    if key == Key.esc:
        # Stop listener
        return False

def run():
    print("RUNNING")
    PressKey(0x38) #Press 8
    ReleaseKey(0x38) 
    time.sleep(0.6)
    PressKey(0x38) #Press 8
    ReleaseKey(0x38) 
    time.sleep(0.6)
    print("Total encounters: ", encounter)
    print("Zephyruffs encountered: ", zeph)

def screen_scan():
    global encounter
    global zeph
    if (pyautogui.locateOnScreen('zephyruff/battle_start.png', confidence = 0.6)) is not None:
        #In battle
        print("In battle")
        ReleaseKey(0x41)
        ReleaseKey(0x44)
        time.sleep(7.5)
        if (pyautogui.locateOnScreen('zephyruff/luma_mark.png', confidence = 0.7)) is not None:
            print("Luma tem detected")
            zeph += 1
            keyboard.wait('-')
            return 1
        elif (pyautogui.locateOnScreen('zephyruff/one_tem_zeph.png', confidence = 0.95)) is not None:
            print("One tem detected: Zephyruff")
            zeph += 1
            encounter += 1
            run()
            return 1
        elif (pyautogui.locateOnScreen('zephyruff/one_tem_pigepic.png', confidence = 0.95)) is not None:
            print("One tem detected: Pigepic")
            encounter += 1
            run()
            return 1
        elif (pyautogui.locateOnScreen('zephyruff/one_tem_paharac.png', confidence = 0.95)) is not None:
            print("One tem detected: Paharac")
            encounter += 1
            run()
            return 1
        elif (pyautogui.locateOnScreen('zephyruff/two_tem_zeph.png', confidence = 0.95)) is not None:
            print("Two tems detected: Both Zephyruff")
            zeph += 2
            encounter += 2
            run()
            return 1
        elif (pyautogui.locateOnScreen('zephyruff/two_tem_zephyruff_pigepic.png', confidence = 0.95)) is not None:
            print("Two tems detected: Zephyruff and Pigepic")
            zeph += 1
            encounter += 2
            run()
            return 1
        elif (pyautogui.locateOnScreen('zephyruff/two_tem_zephyruff_paharac.png', confidence = 0.95)) is not None:
            print("Two tems detected: Zephyruff and Paharac")
            zeph += 1
            encounter += 2
            run()
            return 1
        else:
            print("Unaccounted for encounter")
            #run()
    elif (pyautogui.locateOnScreen('default/run.png', confidence = 0.6)) is not None:
        print("Unstucking")
        ReleaseKey(0x41)
        ReleaseKey(0x44)
        run()
    

def start():
    while keyboard.is_pressed('`') != True:
        r = random.uniform(0,1)
        PressKey(0x41)  #Press A
        time.sleep(r)
        

        if screen_scan() == 0:
            return None
        ReleaseKey(0x41)
        r = random.uniform(0,1)

        PressKey(0x44)  #Press D
        time.sleep(r)
        if screen_scan() == 0:
            return None     
        ReleaseKey(0x44)


if __name__ == "__main__":
    while True:
        keyboard.wait('=')
        start()
