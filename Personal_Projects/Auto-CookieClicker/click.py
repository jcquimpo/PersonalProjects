import time
import pyautogui

print("Starting in 5 seconds...")
time.sleep(5)

try: 
    while True:
        pyautogui.click()
        time.sleep(0.1)  # Adjust the delay as needed
except KeyboardInterrupt:
    print("Script stopped by user.")
