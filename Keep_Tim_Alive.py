from random import randint as randint
import pyautogui as pag
from time import sleep as wait
from screeninfo import get_monitors
import datetime
import time
import os

file = open("settings.txt", "r")
content = file.read()
file.close()

settings = {}
content = content.split('\n')
for l in content:
    if ('#' in l) or (len(l)<1): continue
    tmp_lst = l.split(' = ')
    settings[str(tmp_lst[0])] = tmp_lst[1]

if len(settings)<3:
    START_TIME = '08:00'
    CUT_OFF_TIME = '17:25'
    AUTO_SHUTDOWN = 'True'
else:
    START_TIME = settings['START_TIME']
    CUT_OFF_TIME = settings['CUT_OFF_TIME']
    AUTO_SHUTDOWN = settings['AUTO_SHUTDOWN']

def conv_time_to_sec(TIME):
    seconds_hms = [3600, 60, 1]
    alarmTime = [int(n) for n in TIME.split(":")]
    alarmSeconds = sum([a*b for a,b in zip(seconds_hms[:len(alarmTime)], alarmTime)])
    return alarmSeconds

def times_up(alarmSeconds):
    now = datetime.datetime.now()
    seconds_hms = [3600, 60, 1]
    currentTimeInSeconds = sum([a*b for a,b in zip(seconds_hms, [now.hour, now.minute, now.second])])
    if (alarmSeconds - currentTimeInSeconds) <= 0: return True
    else: return False

def move_mouse_for(duration=4,cycle=10,perpetual=False,TIME="17:30"):
    if pag.FAILSAFE: pag.FAILSAFE = False
    max_y = get_monitors()[0].height
    max_x = get_monitors()[0].width
    param_x = [int(max_x*0.25), int(max_x/2), int(max_x*0.75), int(max_x)]
    param_y = [int(max_y*0.25), int(max_y/2), int(max_y*0.75), int(max_y)]
    mid_y = param_y[1]
    mid_x = param_x[1]
    cur_cycle = 0
    
    pag.moveTo(mid_x,mid_y,duration=0.2)
    alarmSeconds = conv_time_to_sec(TIME)
    
    while True:
        if times_up(alarmSeconds): break
        
        cur_cycle += 1
        x = randint(600,650)
        y = randint(500,600)
        pag.moveTo(x,y,duration=0.2)
        wait(duration)
        pag.click()
        
        if (not perpetual) and (cur_cycle == cycle): return

while True:
    startSeconds = conv_time_to_sec(START_TIME)
    if times_up(startSeconds): break 
move_mouse_for(perpetual=True,TIME=CUT_OFF_TIME)

if AUTO_SHUTDOWN:
    os.system("shutdown /s /t 1")