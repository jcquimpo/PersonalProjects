import time
import pyautogui
import pygetwindow as gw
import sys

CLICK_INTERVAL = 0.05     # seconds between clicks (20 CPS)
STARTUP_DELAY  = 5        # seconds to wait after focusing the window

# Cookie position — run the helper below first to find your coordinates
COOKIE_X = None   # e.g. 150
COOKIE_Y = None   # e.g. 400


def find_and_focus_window():
    """Focus the browser window that has Cookie Clicker open."""
    windows = gw.getWindowsWithTitle("Cookie Clicker")

    if not windows:
        print("Could not find Cookie Clicker window. Is it open in your browser?")
        return False

    win = windows[0]
    win.activate()
    print(f"Focused window: {win.title}")
    return True


def get_cookie_position():
    """
    Interactive helper — move your mouse over the cookie and press Enter.
    Run this once to find COOKIE_X / COOKIE_Y, then hard-code them above.
    """
    print("Move your cursor over the BIG COOKIE and press Enter...")
    input()
    x, y = pyautogui.position()
    print(f"Cookie is at: x={x}, y={y}")
    print(f"Set COOKIE_X = {x} and COOKIE_Y = {y} at the top of the script.")
    return x, y


def main():
    global COOKIE_X, COOKIE_Y

    pyautogui.FAILSAFE = True   # move mouse to top-left corner to abort

    # Step 1: find cookie position 
    if COOKIE_X is None or COOKIE_Y is None:
        print("Cookie position not configured.")
        COOKIE_X, COOKIE_Y = get_cookie_position()

    # Step 2: focus the game window
    print("Focusing Cookie Clicker window...")
    if not find_and_focus_window():
        sys.exit(1)

    print(f"Starting in {STARTUP_DELAY} seconds — switch to the game now!")
    time.sleep(STARTUP_DELAY)

    # Step 3: autoclick 
    print(f"Clicking ({COOKIE_X}, {COOKIE_Y}) at {1/CLICK_INTERVAL:.0f} CPS. "
          "Move mouse to top-left corner to stop.")
    try:
        while True:
            pyautogui.click(COOKIE_X, COOKIE_Y)
            time.sleep(CLICK_INTERVAL)
    except KeyboardInterrupt:
        print("\nStopped by Ctrl+C.")


if __name__ == "__main__":
    main()