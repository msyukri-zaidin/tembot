import ctypes
from ctypes import wintypes
import time
import pyautogui
import keyboard
import random

caught = 0
halfway = False
RTB = False

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

def halfway_point():
    time.sleep(5)
    PressKey(0x49) #Press I
    ReleaseKey(0x49) 
    time.sleep(1)

    PressKey(0x53) #Press S
    ReleaseKey(0x53) 
    time.sleep(1)

    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(1)

    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(1)

    PressKey(0x1B) #Press ESC
    ReleaseKey(0x1B) 
    time.sleep(0.7)

    PressKey(0x1B) #Press ESC
    ReleaseKey(0x1B) 
    time.sleep(0.7) 

    PressKey(0x1B) #Press ESC
    ReleaseKey(0x1B) 
    time.sleep(0.7)     

    global halfway
    halfway = False  

def walk():
    #Go to shop
    PressKey(0x57)  #Press W
    time.sleep(0.5)
    ReleaseKey(0x57)

    PressKey(0x44)  #Press D
    time.sleep(0.75)
    ReleaseKey(0x44)  

    PressKey(0x57)  #Press W
    time.sleep(0.5)
    ReleaseKey(0x57)   

    #Buy temcards
    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(1)

    PressKey(0x46) #Press F
    ReleaseKey(0x46) 

    time.sleep(1)

    PressKey(0x53)  #Press S
    ReleaseKey(0x53)
    time.sleep(0.2)

    PressKey(0x53)  #Press S
    ReleaseKey(0x53)    
    time.sleep(0.2)

    PressKey(0x46) #Press F
    ReleaseKey(0x46)

    time.sleep(0.2)

    PressKey(0x44)  #Press D
    time.sleep(2)
    ReleaseKey(0x44)
    time.sleep(0.2)

    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.5)

    PressKey(0x1B) #Press ESC
    ReleaseKey(0x1B) 
    time.sleep(0.6)     

    #Go to healing station

    PressKey(0x53)  #Press S
    time.sleep(0.5)
    ReleaseKey(0x53) 

    PressKey(0x41)  #Press A
    time.sleep(1.3)
    ReleaseKey(0x41)

    PressKey(0x57)  #Press W
    time.sleep(0.6)
    ReleaseKey(0x57)  

    PressKey(0x44)  #Press D
    time.sleep(0.1)
    ReleaseKey(0x44)  

    PressKey(0x46) #Press F
    ReleaseKey(0x46)     

    #Healing tems
    time.sleep(8)

    #Leave healing station
    PressKey(0x53)  #Press S
    time.sleep(0.9)
    ReleaseKey(0x53)    

    PressKey(0x44)  #Press D
    time.sleep(0.5)
    ReleaseKey(0x44) 

    PressKey(0x53)  #Press S
    time.sleep(0.4)
    ReleaseKey(0x53)    

    #Walk to cave
    PressKey(0x41)  #Press A
    time.sleep(2.3)
    ReleaseKey(0x41)

    PressKey(0x53)  #Press S
    time.sleep(0.5)
    ReleaseKey(0x53)  

    PressKey(0x41)  #Press A
    time.sleep(1.3)
    ReleaseKey(0x41)

    PressKey(0x57)  #Press W
    time.sleep(0.9)
    ReleaseKey(0x57)  

    PressKey(0x57)  #Press W
    time.sleep(3)
    ReleaseKey(0x57)  


def return_to_base():
    time.sleep(5)
    PressKey(0x49) #Press I
    ReleaseKey(0x49) 
    time.sleep(0.6)

    PressKey(0x53) #Press S
    ReleaseKey(0x53) 
    time.sleep(0.6)

    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)

    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(3)

    global RTB
    RTB = False
    walk()

def catch_tem():
    global RTB
    global halfway
    PressKey(0x37) #Press 7
    ReleaseKey(0x37) 
    time.sleep(0.6)

    if (pyautogui.locateOnScreen('default/halfway.png')) is not None:
        halfway = True
        print("HALFWAY TRUE")
    elif (pyautogui.locateOnScreen('default/RTB2.png')) is not None:
        RTB = True
        print("RETURN TO BASE")
    elif (pyautogui.locateOnScreen('default/RTB.png')) is not None:
        RTB = True
        print("RETURN TO BASE")

    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)

    PressKey(0x37) #Press 7
    ReleaseKey(0x37) 
    time.sleep(0.6)

    if (pyautogui.locateOnScreen('default/halfway.png')) is not None:
        halfway = True
        print("HALFWAY TRUE")
    elif (pyautogui.locateOnScreen('default/RTB2.png')) is not None:
        RTB = True
        print("RETURN TO BASE")
    elif (pyautogui.locateOnScreen('default/RTB.png')) is not None:
        RTB = True
        print("RETURN TO BASE")
    
    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)



    while True:
        if (pyautogui.locateOnScreen('default/run.png', confidence = 0.6)) is not None:
            catch_tem()
        elif (pyautogui.locateOnScreen('default/caught2.png', confidence = 0.6)) is not None:
            break
        elif (pyautogui.locateOnScreen('default/in_world.png', confidence = 0.8)) is not None:
            break
        elif (pyautogui.locateOnScreen('default/stuck.png', confidence = 0.8)) is not None:
            print("Unstucking")
            PressKey(0x46) #Press F
            ReleaseKey(0x46) 
            time.sleep(0.6)

def analyse_tem():
    if (pyautogui.locateOnScreen('default/50sv.png', confidence = 0.6)) is not None:
        PressKey(0x46) #Press F
        ReleaseKey(0x46) 
        time.sleep(1)
    else:
        PressKey(0x44) #Press D
        ReleaseKey(0x44) 
        time.sleep(0.6)        
        PressKey(0x46) #Press F
        ReleaseKey(0x46) 
        time.sleep(0.6)      
        PressKey(0x46) #Press F
        ReleaseKey(0x46) 
        time.sleep(3)            

    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6) 

def run():
    print("RUNNING")
    PressKey(0x38) #Press 8
    ReleaseKey(0x38) 
    time.sleep(0.6)
    PressKey(0x38) #Press 8
    ReleaseKey(0x38) 
    time.sleep(0.6)

def single_battle():
    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)
    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)

    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)
    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)

    while True:
        if (pyautogui.locateOnScreen('default/run.png', confidence = 0.6)) is not None:
            catch_tem()
            analyse_tem()
            break
        elif (pyautogui.locateOnScreen('default/stuck.png', confidence = 0.8)) is not None:
            print("Unstucking")
            PressKey(0x46) #Press F
            ReleaseKey(0x46) 
            time.sleep(0.6)

def catch_tem2():
    global RTB
    global halfway
    PressKey(0x37) #Press 7
    ReleaseKey(0x37) 
    time.sleep(0.6)

    if (pyautogui.locateOnScreen('default/halfway.png')) is not None:
        halfway = True
        print("HALFWAY TRUE")
    elif (pyautogui.locateOnScreen('default/RTB2.png')) is not None:
        RTB = True
        print("RETURN TO BASE")
    elif (pyautogui.locateOnScreen('default/RTB.png')) is not None:
        RTB = True
        print("RETURN TO BASE")  
    elif (pyautogui.locateOnScreen('default/stuck.png', confidence = 0.8)) is not None:
        print("Unstucking")
        PressKey(0x46) #Press F
        ReleaseKey(0x46) 
        time.sleep(0.6)      

    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)

    PressKey(0x53) #Press S
    ReleaseKey(0x53) 
    time.sleep(0.6)

    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)

    PressKey(0x37) #Press 7
    ReleaseKey(0x37) 
    time.sleep(0.6)

    if (pyautogui.locateOnScreen('default/halfway.png')) is not None:
        halfway = True
        print("HALFWAY TRUE")
    elif (pyautogui.locateOnScreen('default/RTB2.png')) is not None:
        RTB = True
        print("RETURN TO BASE")
    elif (pyautogui.locateOnScreen('default/RTB.png')) is not None:
        RTB = True
        print("RETURN TO BASE")
    
    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)

    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)


def barrage():
    #First turn attacks
    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)
    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)

    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)
    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)

    while True:
        if (pyautogui.locateOnScreen('default/run.png', confidence = 0.6)) is not None:
            break
        elif (pyautogui.locateOnScreen('default/stuck.png', confidence = 0.8)) is not None:
            print("Unstucking")
            PressKey(0x46) #Press F
            ReleaseKey(0x46) 
            time.sleep(0.6)

    #Second turn attack other enemy
    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)
    PressKey(0x57) #Press W
    ReleaseKey(0x57) 
    time.sleep(0.6)
    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)

    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)
    PressKey(0x46) #Press F
    ReleaseKey(0x46) 
    time.sleep(0.6)

def double_battle():
    print("Initiating first barrage")
    barrage()

    print("Waiting for turn..")
    #Wait for turn
    while True:
        if (pyautogui.locateOnScreen('default/run.png', confidence = 0.6)) is not None:
            break
        elif (pyautogui.locateOnScreen('default/stuck.png', confidence = 0.8)) is not None:
            PressKey(0x46) #Press F
            ReleaseKey(0x46) 
            time.sleep(0.6)

    print("Initiating catch sequence")
    catch_tem2()

    global caught
    print("Catching tem..")
    while True:
        #If this, new turn - likely no tem caught if this happens
        if (pyautogui.locateOnScreen('default/run.png', confidence = 0.6)) is not None:
            print("No tem caught on first wind")
            break
        if (pyautogui.locateOnScreen('default/inter.png', confidence = 0.6)) is not None:
            PressKey(0x46) #Press F
            ReleaseKey(0x46) 
            time.sleep(0.6)
        #else if this, tem caught
        elif (pyautogui.locateOnScreen('default/caught2.png', confidence = 0.8)) is not None:
            print("Tem has been caught")
            analyse_tem()
            caught += 1
            print("Tem caught: ", caught)            
            if caught == 2:
                break
        elif (pyautogui.locateOnScreen('default/stuck.png', confidence = 0.8)) is not None:
            PressKey(0x46) #Press F
            ReleaseKey(0x46) 
            time.sleep(0.6)
        elif (pyautogui.locateOnScreen('default/in_world.png', confidence = 0.8)) is not None:
            return None
        
    if caught == 0:
        print("Initiating second barrage")
        barrage()
        #Wait for turn
        print("Waiting for turn..")
        while True:
            if (pyautogui.locateOnScreen('default/run.png', confidence = 0.6)) is not None:
                break
            elif (pyautogui.locateOnScreen('default/stuck.png', confidence = 0.8)) is not None:
                print("Unstucking")
                PressKey(0x46) #Press F
                ReleaseKey(0x46) 
                time.sleep(0.6)
        #Catch tem
        catch_tem2()
        while True:
            print("SECOND WIND")
            #If this, no tem caught on second wind, run away
            if (pyautogui.locateOnScreen('default/run.png', confidence = 0.6)) is not None:
                print("SECOND WIND: No tem caught, running away")
                run()
                break
            if (pyautogui.locateOnScreen('default/inter.png', confidence = 0.6)) is not None:
                PressKey(0x46) #Press F
                ReleaseKey(0x46) 
                time.sleep(0.6)
            #else if this, tem caught
            elif (pyautogui.locateOnScreen('default/caught2.png', confidence = 0.8)) is not None:
                print("Tem has been caught")
                analyse_tem()
                caught += 1
                print("In second wind, caught: ", caught)
                if caught == 2:
                    break
            elif (pyautogui.locateOnScreen('default/stuck.png', confidence = 0.8)) is not None:
                PressKey(0x46) #Press F
                ReleaseKey(0x46) 
                time.sleep(0.6)
            elif (pyautogui.locateOnScreen('default/in_world.png', confidence = 0.8)) is not None:
                return None


    
    if caught == 1:
        print("CAUGHT 1 BUT NEED TO CATCH ANOTHER ONE")
        catch_tem()
        analyse_tem()
    caught = 0




    
def screen_scan():
    if (pyautogui.locateOnScreen('default/battle_start2.png', confidence = 0.6)) is not None:
        #In battle
        print("In battle")
        ReleaseKey(0x41)
        ReleaseKey(0x44)
        time.sleep(7.5)
        if (pyautogui.locateOnScreen('default/one_tem.png', confidence = 0.75)) is not None:
            print("One tem detected")
            single_battle()
            return 1
        if (pyautogui.locateOnScreen('default/one_tem2.png', confidence = 0.75)) is not None:
            print("One tem detected")
            single_battle()
            return 1
        elif (pyautogui.locateOnScreen('default/two_tem.png', confidence = 0.6)) is not None:
            print("Two tems detected")
            double_battle()
            return 1
        elif (pyautogui.locateOnScreen('default/two_tem2.png', confidence = 0.6)) is not None:
            print("Two tems detected")
            double_battle()
            return 1
        elif (pyautogui.locateOnScreen('default/two_tem3.png', confidence = 0.6)) is not None:
            print("Two tems detected")
            double_battle()
            return 1

def start():
    global halfway
    global RTB
    while keyboard.is_pressed('`') != True:
        r = random.uniform(0,1)
        PressKey(0x41)  #Press A
        time.sleep(r)
        

        if screen_scan() == 0:
            return None
        if halfway == True:
            halfway_point()
        if RTB == True:
            return_to_base()
        ReleaseKey(0x41)
        global caught
        caught = 0
        r = random.uniform(0,1)

        PressKey(0x44)  #Press D
        time.sleep(r)
        if screen_scan() == 0:
            return None
        if halfway == True:
            halfway_point()
        if RTB == True:
            return_to_base()        
        ReleaseKey(0x44)


if __name__ == "__main__":
    while True:
        keyboard.wait('=')
        start()


'''s
ws
'''