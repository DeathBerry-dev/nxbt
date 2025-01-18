import time
from random import randint

import nxbt
from nxbt import Buttons
from nxbt import Sticks
#MACROS
DIALOG_SETUP = """
0.1s
L_STICK@-50+50 0.1s
A 0.1s
4s
A 0.1s
1s
"""#left on "I would like to print something"
NAVIGATE_TIME = """
1s
HOME 0.1s
5s
DPAD_DOWN 0.1s
0.5s
LOOP 5
    DPAD_RIGHT 0.1s
    0.1s
1s
A  0.1s
1s
DPAD_DOWN 3s
1s
A 0.1s
1s
LOOP 3
    DPAD_DOWN 0.1s
    0.1s

LOOP 2
    DPAD_DOWN 0.1s
0.1s

LOOP 2
    DPAD_DOWN 0.1s
    0.1s
A 0.1s
1s
LOOP 2
    DPAD_DOWN 0.1s
    0.1s
0.1s
A 0.1s
1s
""" #left on date and time
TIMING = """
0.1s
HOME 0.1s
1s
A 0.1s
1s
""" #left in game for timer
PRINT_ITEM = """
15s
X 0.1s
1s
A 0.1s
7s
A 0.1s
20s
A 0.1s
1s
A 0.1s
1s
LOOP 8
    B 0.1s
    0.9s
""" #left looking at printer
PRINT_ITEM_R = """
15s
R 0.1s
1s
X 0.1s
1s
A 0.1s
7s
A 0.1s
20s
A 0.1s
1s
A 0.1s
1s
LOOP 8
    B 0.1s
    0.9s
""" #left looking at printer
PRINT_ITEM_L = """
15s
L 0.1s
1s
X 0.1s
1s
A 0.1s
7s
A 0.1s
20s
A 0.1s
1s
A 0.1s
1s
LOOP 8
    B 0.1s
    0.9s
""" #left looking at printer
TURN_OFF = """
1s
HOME 0.1s
1s
DPAD_DOWN 0.1s
0.5s
LOOP 4
    DPAD_RIGHT 0.1s
    0.3s
0.5s
A  0.1s
0.1s
A  0.1s
"""
def random_colour():
    return [
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
    ]
def generate_seeds(): #creates Dict of date/time for items/bonus
    with open("Pokemon_Seeds.csv", "r") as seeds:
        ref = {}
        for item in seeds:
            parts = item.strip()
            parts = parts.split(";")
            ref[parts[-1]] = int(parts[2]), int(parts[1]), int(parts[0]), int(parts[3]), int(parts[4]), int(parts[5])
        return ref
def item_input(): #Select item
    print(f"Avaliable items:{seed_name()}")
    while True:
        item_select = input(f"Type which item you would like:")
        if item_select in seed:
            return seed[item_select]
        else:
            print("incorrect input")
def mode_set(input_item, mode): #sets mode based on item selected
    if mode == 1:
        return bonus_check(input_item)
    elif mode == 5:
        return input_item
    else:
        raise ValueError
def bonus_check(item): #selects what bonus is required based on item
    if item in balls:
        return 12, 1, 2025, 23, 35, 8
    else:
        return 11, 1, 2025, 21, 59, 9
def ball_list(): #set bonus select filter
    ref = []
    for item in seed:
        if "Ball" in item:
            ref.append(item)
    return ref
def repeat_amount(): #sets amount of repeats to be done
    while True:
        repeat = int(input(f"Type how many times to repeat:"))
        try:
            if abs(repeat) > 0:
                return abs(repeat)
        except:
            pass
        print("incorrect input")
def seed_name(): #creates list of names for items to input
    ref = []
    for name in seed:
        ref.append(name)
    return ref

def time_change_setup(current_time, item): #changes date time settings
    print("changing time settings")
    date_change(current_time[0], item[0]) #day
    nx.press_buttons(controller_index, [Buttons.DPAD_RIGHT], block=True)
    date_change(current_time[1], item[1]) #month
    nx.press_buttons(controller_index, [Buttons.DPAD_RIGHT], block=True)
    date_change(current_time[2], item[2]) #year
    nx.press_buttons(controller_index, [Buttons.DPAD_RIGHT], block=True)
    date_change(current_time[3], item[3]) #hour
    nx.press_buttons(controller_index, [Buttons.DPAD_RIGHT], block=True)
    date_change(current_time[4], item[4]) #minute
    nx.press_buttons(controller_index, [Buttons.DPAD_RIGHT], block=True)
    print(f"time set to {item}")
def date_change(current, target): #inputs for date/time changes
    dif = current - target
    if dif > 0:
        for repeat in range(0, abs(dif)):
            nx.press_buttons(controller_index, [Buttons.DPAD_DOWN], block=True)
    elif dif < 0:
        for repeat in range(0, abs(dif)):
            nx.press_buttons(controller_index, [Buttons.DPAD_UP], block=True)
    elif dif == 0:
        return
    else:
        return ValueError
def timer(item): #timer TM
    print(f"countdown target {item}s")
    global start_flag
    timing = float(item) - delay
    nx.press_buttons(controller_index, [Buttons.A], block=True)#start countdown
    start_flag = time.perf_counter()
    macro_id = nx.macro(controller_index, TIMING, block=False)
    while True:
        if time_check() >= timing:
            nx.press_buttons(controller_index, [Buttons.A])
            print(f"timer completed at {time_check():.6f}")
            break
    print("<Menu>")
def update_current(item): #keeps track of current date time setting
    global current_time #going to change current 
    print(time_check())
    runtime = time.strftime("%M:%S", time.gmtime(time_check())) #time thats lapsed
    print(f"runtime was {runtime}s")
    runtime_parts = runtime.split(":") #split into min, sec
    print(f"{int(item[4])}+{int(runtime_parts[0])}")
    minute_update = int(item[4]) + int(runtime_parts[0])
    if minute_update >= 60:
        minute_update -= 60
        time_elapsed = tuple((item[0], item[1], item[2], (item[3]+1), minute_update, 0))
        #print("added an hour")
    else:
        time_elapsed = tuple((item[0], item[1], item[2], item[3], minute_update, 0))
        #print("only added minutes")
    current_time = time_elapsed
    print(f"time set to {current_time}")
def print_job(mode): #keeps track of Job amount is set to
    global job_set
    if job_set < mode:
        print("Setting Job to 5\nPrinting...")
        macro_id = nx.macro(controller_index, PRINT_ITEM_R, block=True) #print item
        job_set = mode
    elif job_set > mode:
        print("setting job to 1\nPrinting...")
        macro_id = nx.macro(controller_index, PRINT_ITEM_L, block=True) #print item
        job_set = mode
    else:
        macro_id = nx.macro(controller_index, PRINT_ITEM, block=True)
def return_default():
    print("returning to default posistion")
    macro_id = nx.macro(controller_index, DIALOG_SETUP, block=True) #sets up Dialog for next print
    print("Returning to Date and Time settings")
    macro_id = nx.macro(controller_index, NAVIGATE_TIME, block=True) #time paused
def print_main(): #main LOOP
    macro_id = nx.macro(controller_index, NAVIGATE_TIME)
    print(f"set date and time to {default_time}")
    input("Press ENTER to continue...")
    #item = item_input()
    item = seed["EXP_Candy_XL"]
    repeat = repeat_amount()
    for i in range(0, repeat):
        print(f"\nPrinting batch {i+1}")
        print("\nsetting up bonus")
        item_print(item, 1)
        print("\nprinting frist batch")
        item_print(item, 5)
        print("\nprinting last batch")
        item_print(item, 5)
    print("\nRepeats have completed")
def item_print(input_item, mode): #setup and print
    item = mode_set(input_item, mode)
    time_change_setup(current_time[:-1], item[:-1])
    timer(item[-1]) #runs timer and returns start_flag
    print_job(mode)
    return_default()
    update_current(item)
def time_check():
    return time.perf_counter() - start_flag

if __name__ == "__main__":
    #set_up
    #Global Variables
    default_time = (1, 1, 2025, 0, 0, 0)
    current_time = default_time
    job_set = 5
    seed = generate_seeds()
    balls = ball_list()
    delay = 1.0006
    #start_flag = 0
    # Init NXBT
    import nxbt

    # Start the NXBT service
    nx = nxbt.Nxbt()

    # Create a Pro Controller and wait for it to connect
    controller_index = nx.create_controller(nxbt.PRO_CONTROLLER)
    nx.wait_for_connection(controller_index)

    print("Connected")
    #player set up intructions
    print("Before continuing please make sure you have completed the following intructions")
    print("Open pokemon and print 1 item with job amount 5")
    print("Turn and talk to NPC and leave on 'I would like to print something'")
    print("Have date and time set to YY:MM:DD 24hour clock")
    print("leave cursor on year")
    print("WARNING: make sure there is no current bonus")
    #Program Starts HERE
    print_main()
    macro_id = nx.macro(controller_index, TURN_OFF)
