# raspberry pi Python program to play some videos for the ITS pumpkin
# Note that this uses "curses" library, so must be run from the command line
from gpiozero import Button
import subprocess, os

from time import sleep
import curses

sensor = Button(4)
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(True)
stdscr.nodelay(True)

# get all of the video files from the Videos directory
filelist = os.listdir(path='/home/pi/Videos/')
filelen = len(filelist)

fileindex = 0

stdscr.clear()

# Launch a process in the background running omxplayer media player showing the
#     simulated jack-o-lantern glowing eyes video.
omx = subprocess.Popen(['omxplayer', '-b', '--loop', '/home/pi/pumpkin.mov'])

# start a loop waiting on keyboard input (the "q" key will quit the program)
#     or input from the IR sensor
key = ''
while key != ord('q'):
    key = stdscr.getch()
    if sensor.is_pressed:
        os.system('killall omxplayer.bin')
        omx = subprocess.call(['omxplayer', '-b', '/home/pi/thanks.mov'])
        vfile = '/home/pi/Videos/' + filelist[fileindex]
        omx = subprocess.Popen(['omxplayer', '-b', vfile])
        sleep(.5)
        fileindex += 1
        if fileindex == filelen: fileindex = 0
    if key == ord('q'):
        os.system('killall omxplayer.bin')
        break
    else:
        stdscr.clear()
        proclist = os.popen('ps -a').read()
        if proclist.find('omxplayer\n') == -1:
            os.system('killall omxplayer.bin')
            subprocess.Popen(['omxplayer', '-b', '--loop', '/home/pi/pumpkin.mov'])

os.system('killall omxplayer.bin')
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
