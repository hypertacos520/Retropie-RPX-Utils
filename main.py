import systemFunctions
import Gamepad
import time
import subprocess
import os

currentDirectory = os.path.dirname(os.path.realpath(__file__))
gamepadType = Gamepad.PS4
buttonHome = 'PS'

def toggle_quick_menu():
    global overlayProcess
    print('HOME_BUTTON')
    isInGame = systemFunctions.is_in_game()
    print(isInGame)
    if isInGame:
        systemFunctions.freeze_processes() #This line is dangerous to run on the dev computer! Make sure to comment out before testing
        print(subprocess.run(['raspi2png', '-p', currentDirectory + '/Resources/Temp/bg.png'], stdout=subprocess.PIPE))
        menuSelection = subprocess.run(['python3', currentDirectory + '/inGameOverlay.py'], stdout=subprocess.PIPE)
        li = list(str(menuSelection).split('\\n'))
        try:
            if int(li[len(li)-2]) == 0:
                systemFunctions.resume_processes()
                print("resume")
            if int(li[len(li)-2]) == 1:
                systemFunctions.terminate_processes()
                print("terminate")
        except:
            systemFunctions.resume_processes()
        del li
        del menuSelection

# Wait for gamepad connection
if not Gamepad.available():
    print('Please connect your gamepad...')
    while not Gamepad.available():
        time.sleep(1.0)
gamepad = gamepadType()
print('Gamepad connected')

#Main loop. Checks to see if the home button is pressed and if proper conditions are met
while(gamepad.isConnected()):
    # Wait for the next event
    eventType, control, value = gamepad.getNextEvent()
    if eventType == 'BUTTON':
        # Button changed
        if control == buttonHome:
            # Exit button (event on press)
            if value:
                print('Home Pressed!')
                toggle_quick_menu()
                #print(inQuickMenu)