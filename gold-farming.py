
# Global imports
import time
import random as random_lib

random = random_lib.random

# Resolution of current screen
resolution = {
    "x": 1382,
    "y": 864
}

positions = {
    'quit_button': [0.3859375, 0.7657407407407407],
    'play_button': [0.5, 0.9157407407407407]
}

# The baseline for wait time between a keystroke press/release,
# mouse click/release, etc
input_wait_interval = 0.3

# Plus or minus delay range
random_delay_range = 1/5

# Instantiate mouse controller object
from pynput.mouse import Button, Controller
mouse = Controller()

# Instantiate keyboard controller object
from pynput.keyboard import Key, KeyCode, Controller
keyboard = Controller()


def get_mouse_pos_ratio():
    mouse_pos_x, mouse_pos_y = mouse.position
    return mouse_pos_x/resolution.get('x'), mouse_pos_y/resolution.get('y')


def get_mouse_pos_from_ratio(x, y):
    return resolution.get('x')*x, resolution.get('y')*y


def get_random_key(keys):
    return random_lib.choice(keys)


# Block execution for set amount of seconds
def wait(duration=0.1):
    time.sleep(duration)
    return duration


# Get plus or minus a random float between 0 and 1
# [fraction] arg divides the random float further
def add_plus_or_minus(start=0, multiplier=1):
    return start + (random()*multiplier)*(1 if random() > 0.5 else -1)


# simulate_wait() -> wait for 0.3s, plus or minus 0.15s
# simulate_wait(3) -> wait for 4s, plus or minus 1s
def simulate_wait(duration=input_wait_interval, multiplier=random_delay_range):
    if multiplier >= duration:
        # temp solution - fix later (figure out order of magnitude of duration)
        multiplier = duration*0.1

    return wait(add_plus_or_minus(duration, multiplier))


def move_cursor(x, *args):
    y = None

    if type(x) is str:
        pos = positions.get(x)
        x = pos[0]
        y = pos[1]

    y = y or [*args][0]

    pos_x, pos_y = get_mouse_pos_from_ratio(x, y)
    mouse.position = (pos_x, pos_y)
    simulate_wait(0.3, 0.1)


def key_press(key, *args):
    keyboard.press(key)
    simulate_wait(*args)
    keyboard.release(key)
    simulate_wait(0.3, 0.1)


def mouse_click(button, *args):
    mouse.press(button)
    simulate_wait(*args)
    mouse.release(button)
    simulate_wait(0.3, 0.1)


def init(delay=5):
    # Wait initial delay time
    wait(delay)

    # Start farming loop
    for x in range(0, 200):

        # Wait before re-entering dungeon
        simulate_wait(2, 0.5)
        key_press(get_random_key(['a', 'd']), 0.3, 0.1)
        key_press(get_random_key(['w', 's']), 0.2, 0.1)
        key_press('x')

        # Wait for dungeon entry, and loading screen
        simulate_wait(16, 0.5)

        # Press 'w' to move forward into battle
        key_press('w', 10)

        # Wait to initiate battle circle and load cards in hand
        # simulate_wait(4, 1)

        # Select the spell
        key_press(Key.right)

        # Delay between selecting the spell and casting the spell
        simulate_wait(0.2, 0.1)

        # Cast the spell
        key_press(Key.space)

        # Wait for spell animation and fight to end
        simulate_wait(35, 1)

        # Open the exit screen
        key_press(Key.esc)

        # Delay between quitting the game
        simulate_wait(1, 0.33)

        # Move cursor to quit button
        move_cursor('quit_button')

        # Click the quit button
        simulate_wait(0.5, 0.2)
        mouse_click(Button.left)

        # Wait for player menu to load
        simulate_wait(4.5, 0.3)

        # Click play button
        move_cursor('play_button')
        mouse_click(Button.left)

        # Wait for player to load back in game
        simulate_wait(4.5, 0.4)


init()


# wait(1)
#
# print(mouse.position)


