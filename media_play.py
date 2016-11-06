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
        # kill any running videos
        os.system('killall omxplayer.bin')
        # play the thank you video
        omx = subprocess.call(['omxplayer', '-b', '/home/pi/thanks.mov'])
        # get the next video in the directory
        vfile = '/home/pi/Videos/' + filelist[fileindex]
        # open a process to play the video in the background
        omx = subprocess.Popen(['omxplayer', '-b', vfile])
        sleep(.5)
        fileindex += 1
        if fileindex == filelen: fileindex = 0
    if key == ord('q'):
        os.system('killall omxplayer.bin')
        break
    else:
        # during this loop, check whether a video is still playing. If not, launch the
        #    simulated "eyes" video (pumpkin.mov)
        stdscr.clear()
        # get the list of process running on the Raspberry Pi
        proclist = os.popen('ps -a').read()
        # note that when an "omxplayer" process is killed, it very often will
        #   persist as a "<defunct>" process. So we search here for an "omxplayer"
        #   process that is not "<defunct>" (ends with a new line character instead).
        #   If no active process is found (one that doesn't end in "omxplayer\n", then
        #      launch the "pumpkin.mov" video. This means that all active videos have completed.
        if proclist.find('omxplayer\n') == -1:
            os.system('killall omxplayer.bin')
            subprocess.Popen(['omxplayer', '-b', '--loop', '/home/pi/pumpkin.mov'])

os.system('killall omxplayer.bin')
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
