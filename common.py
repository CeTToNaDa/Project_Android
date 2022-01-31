import sys
import subprocess
import time
import os
from uiautomator import Device


deviceSerial = subprocess.check_output("adb devices -l | grep SM | awk '{print $1}'", shell=True).decode('utf-8').rstrip()
device = Device(deviceSerial)
testResult = True

all_Aps = ["Play Store", "Maps", "Chrome", "Messages", "Camera", "Clock", "Contacts", "Settings", "Calendar", "Play Music", "Samsung Notes"]


class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def infoMessage(message):
    print(colors.YELLOW +"\n[Info]  %s"%(message) + colors.END)


def successMessage(message):
    print(colors.GREEN +"\n[Success]  %s [✔]\n"%(message) + colors.END)


def errorMessage(message):
    global testResult
    testResult = False
    print(colors.RED +"\n[Error]  %s [✘]\n"%(message) + colors.END)


def testPassedMessage():
    print(colors.BLUE + colors.BOLD + "---------------------------")
    print("┃" + colors.GREEN + colors.BOLD + "\tTest Passed\t  " + colors.BLUE + "┃")
    print("---------------------------\n" + colors.END)
    sys.exit(0)


def testFailedMessage():
    print(colors.BLUE + colors.BOLD + "---------------------------")
    print("┃" + colors.RED + colors.BOLD + "\tTest Failed\t  " + colors.BLUE + "┃")
    print("---------------------------\n" + colors.END)
    sys.exit(1)


def testResultMessage():
    if testResult:
        testPassedMessage()
    else:
        testFailedMessage()


def unlock_phone():
    if device.screen == "off":
        device.screen.on()
    screen_state = subprocess.check_output("adb -s " + deviceSerial + " shell dumpsys nfc | grep \'mScreenState=\'", shell=True).decode('utf-8').rstrip()
    if "ON_LOCKED" in screen_state:
        device.swipe(700, 700, 100, 100)


def go_home():
    subprocess.run("adb -s " + deviceSerial + " shell input keyevent 3", shell=True)
    time.sleep(1)
    if device.exists(className="com.android.launcher3.home.view.ui.workspace.Workspace"):
        print("Home accesed")
    else:
        testFailedMessage()


def go_menu():
    go_home()
    time.sleep(1)
    device.swipe(100, 100, 900, 900)
    for i in range(5):
        if device.exists(resourceId="com.sec.android.app.launcher:id/apps_page_indicator", descriptionContains="Page 1"):
            print("Menu open at first page")
            break
        else:
            device.swipe(100, 500, 600, 500)


def open_app_from_menu(app):
    go_menu()
    for i in range(5):
        if device.exists(text=app):
            print("App " + app + " founded. Open it")
            break
        else:
            device.swipe(600, 500, 100, 500)
    if i != 4:
        device(text=app).click()
    else:
        errorMessage("Aplication " + app + " could not be found")


def reboot():
    subprocess.run("adb -s " + deviceSerial + " reboot", shell=True)
    for i in range(30):
        time.sleep(2)
        test = subprocess.check_output("adb devices -l | grep SM | awk '{print $1}'", shell=True).decode('utf-8').rstrip()
        if test == deviceSerial:
            successMessage("Reboot succesful")
            break
        elif i == 29:
            errorMessage("Phone do not reboot")
            testFailedMessage()


def activate_bluetooth():
    subprocess.run("adb -s " + deviceSerial + " shell am start -a android.settings.BLUETOOTH_SETTINGS", shell=True)
    if device.exists(text="Bluetooth, Off"):
        device(text="Bluetooth, Off").click()
    if device.exists(text="Bluetooth, On"):
        successMessage("Bluetooth activate")
    else:
        errorMessage("Bluetooth not activate")
        testFailedMessage()


def activate_wifi():
    subprocess.run("adb -s " + deviceSerial + " shell am start -a android.intent.action.MAIN -n com.android.settings/.wifi.WifiSettings", shell=True)
    if device.exists(text="Wi-Fi, Off"):
        device(text="Wi-Fi, Off").click()
        time.sleep(2)
    if device.exists(text="Wi-Fi, On"):
        successMessage("Wi-Fi, On")
    else:
        errorMessage("Wi-Fi, Off")
        testFailedMessage()


def run_antutu():
    if device.exists(text="Enable 64-bit", clickable="true"):
        device(text="Enable 64-bit", clickable="true").click()
    if device.exists(text="Settings"):
        device(text="Settings").click()
    if device.exists(text="Off"):
        device(text="Off").click()


def start_camera():
    subprocess.run("adb -s " + deviceSerial + " shell input keyevent 27", shell=True)
    if device.exists(text="Shutter", packageName="com.sec.android.app.camera"):
        successMessage("Camera app is open")
    else:
        testFailedMessage()


def install_app(app_name):
    result = os.system("adb -s " + deviceSerial + " install " + app_name)
    if int(result) != 0:
        errorMessage(f"Couldn't Install {app_name}")


def test_antutu():
    subprocess.run("adb -s " + deviceSerial + " shell am start -a android.intent.action.MAIN -n com.antutu.ABenchMark/.ABenchMarkStart", shell=True)
    time.sleep(10)
    if device.exists(resourceId="com.antutu.ABenchMark:id/download_from_title") and device.exists(text="Cancel"):
        print("Test")
        device(text="Cancel", clickable="true").click()
    time.sleep(2)
    if device.exists(text="Test", clickable="true"):
        device(text="Test", clickable="true").click()
    device(textContains="Non-verified").wait.exists(timeout=600)
    raw_value = device(textContains="Non-verified").info["text"].split(": ")[1]
    print(raw_value)
    if raw_value < 60000:
        errorMessage("Score point under 60000 limit")
    go_menu()


def test():
    raw_value = device(textContains="Non-verified").info["text"].split(": ")[1]
    print(raw_value)
