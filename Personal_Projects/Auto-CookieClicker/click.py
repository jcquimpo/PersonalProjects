import time
import pyautogui

print("Starting in 10 seconds...")
time.sleep(10)

try: 
    while True:
        pyautogui.click()
        time.sleep(0.1)  # Adjust the delay as needed
except KeyboardInterrupt:
    print("Script stopped by user.")
