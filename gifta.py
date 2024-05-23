import gifToASCII
import subprocess
import os
import time
import threading

# the art directory MUST contain the gif the user will be converting
# if you are modifying this code it should be easy to change this
os.chdir("art")
subprocess.run(['powershell', 'ls'], shell=False) # displays the imgs in the images folder bc why not
os.chdir("..")


# pretty self explanatory
fileName = input("enter file name (wihout.gif): ")

# from the stuff i've learnt through research of ASCII art
# the background does really matter since the characters that represent certain light values
# must be reversed; you cant write in black ink on black paper right?
background = input("are you displaying it on a dark or light background [d,l]?\n")

outputDir = './artworks' # defualt output directory

# creating object for gif
giftoasc = gifToASCII.gifToASCII(fileName=fileName, background=background, outputDir=outputDir)

# this function is the inteded way of using this script
# to be honest i have not tried any other combinations
# so try different combinations out with caution else they may cause some errors
def actualFunction():
    giftoasc.gifSplice()
    giftoasc.framesToASCII()
    giftoasc.ASCIIToFrames()
    giftoasc.gifMerge()

# this is for class there's no need for this but I want this
# so i'll have it :D
def animate():
    animation = "|/-\\"
    idx = 0
    while not done:
        print(f'please wait! {animation[idx % len(animation)]}...', end="\r")
        idx += 1
        time.sleep(0.1)

# simple threading to have both the animation function
# and gif conversion running at the same time
done = False

gifToASCIIThread = threading.Thread(target=actualFunction)
gifToASCIIThread.start()

animationThread = threading.Thread(target=animate)
animationThread.start()

gifToASCIIThread.join()
done = True

animationThread.join()

print("done!")