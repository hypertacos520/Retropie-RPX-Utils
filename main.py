import systemFunctions, time, os
import graphicOverlay as go
try:
    import Gamepad
    controllerType = Gamepad.PS4    #Can be changed based on your desired controller input
    buttonHome = 'PS'               #Will need to be updated if controller type is changed
    keyboardInput = None
except:
    import keyboard
    keyboardInput = 1
    print("Gamepad Library Missing. Falling back to Keyboard Input.")

currentDirectory = os.path.dirname(os.path.realpath(__file__))

def toggle_quick_menu():
    isInGame = systemFunctions.is_in_game()
    print("Is a game currently running?: " + str(isInGame))
    if isInGame:
        systemFunctions.freeze_processes() #This line is dangerous to run on the dev computer! Make sure to comment out before testing
        try:
            systemFunctions.take_screenshot(0) #Does not work on dev pc
        except:
            pass
        menuSelection = go.ingame_overlay_main(isInGame) #New overlay function
        try:
            if menuSelection == 0:
                print("Resuming Current Application...")
                systemFunctions.resume_processes()
            elif menuSelection == 1:
                print("Exiting Current Application...")
                systemFunctions.terminate_processes()
            else:
                print("No Valid Input Made By User. Resuming Current Application...")
                systemFunctions.resume_processes()
        except:
            print("Menu Failed During Execution. Resuming Current Application...")
            systemFunctions.resume_processes()
        del menuSelection
        del isInGame
    else:
        systemFunctions.freeze_frontend()
        try:
            systemFunctions.take_screenshot(0) #Does not work on dev pc
        except:
            pass
        menuSelection = go.ingame_overlay_main(isInGame) #New overlay function
        if menuSelection == 0:
            systemFunctions.resume_frontend()
        else:
            print("No Valid Input Made By User. Resuming Current Application...")
            systemFunctions.resume_frontend()

#Main loop for controller input
def controller_loop():
    while(gamepad.isConnected()):
        try:
            # Wait for the next event
            eventType, control, value = gamepad.getNextEvent()
            if eventType == 'BUTTON':
                # Button changed
                if control == buttonHome:
                    # Exit button (event on press)
                    if value:
                        toggle_quick_menu()
        except:
            pass

#Main loop for keyboard input
def keyboard_loop():
    while(1):
        if keyboard.is_pressed('0'):
            toggle_quick_menu()
            #print(inQuickMenu)
            while(1):
                if keyboard.is_pressed('0'):
                    continue #Ensures button has been released before performing another action
                else:
                    break
                    
# Decide on input method
# Controller Input is the Default
if(keyboardInput):
    keyboard_loop()
else:
    controllerDisconnectCheck = 1
    while(1):
        if not Gamepad.available():
            print('Awaiting Controller Connection...')
            if(not controllerDisconnectCheck):
                os.popen("python3 notification.py 1 Disconnected") #This is a little inefficient but it works 
                # go.send_system_notification(1, "Disconnected")
                controllerDisconnectCheck = 1
            while not Gamepad.available():
                time.sleep(1.0)
        gamepad = controllerType()
        print('Controller Connected!')
        controllerDisconnectCheck = 0
        os.popen("python3 notification.py 1 Connected") #This is a little inefficient but it works 
        # go.send_system_notification(1, "Connected")
        controller_loop()