import pygame, os, gc
import systemFunctions as sf
from pygame.locals import *
from multiprocessing import Process, Queue
try:
    import pydispmanx
except:
    print("pydispmanx Not Available. Reverting to Default.")

#The following script is used to render pygame interfaces as overlays 
#over any running process with help from raspberry pi DispmanX layers.
#The way the script is coded, modifications can be made and tested on
#a development machine using the standard pygame interface while using
#DispmanX layers on a raspberry pi.

#User Modifiable Variables
ManXLayerNum = 10 #DispmanX layer number
cursorColor = (16, 174, 190) #Cursor color in In-Game Menu
primaryColor = (81, 81, 81) #Button color for In-Game Menu

#Dynamic Variables
currentDir = os.path.dirname(os.path.realpath(__file__)) #Dynamically find file directory

#Other Variable Definitions
pyManXLayer = None

#Create Surfaces for PyGame to run on
def init_pygame_runtime(dispmanXLayerOffset, fontModifier = 35):
    global screenX
    global screenY
    global pyManXLayer
    global screen
    global font
    global mainClock
    global ManXLayerNum
    global Joystick
    global releaseCheck

    #If DispmanX is present...
    try:
        screenX, screenY = pydispmanx.getDisplaySize() #Dynamically Get Raspberry Pi Display Size
        pyManXLayer = pydispmanx.dispmanxLayer(ManXLayerNum + dispmanXLayerOffset)
        screen = pygame.image.frombuffer(pyManXLayer, pyManXLayer.size, 'RGBA')
    #Otherwise...
    except: 
        screenX = 800 #Screen X dimension when pydispmanx is not present
        screenY = 480 #Screen Y dimension when pydispmanx is not present
        screen = pygame.display.set_mode((screenX, screenY),0,32)

    pygame.init()
    font = pygame.font.SysFont(pygame.font.get_default_font(), int(screenX/fontModifier)) #Dynamically set font size
    mainClock = pygame.time.Clock() #Initialize PyGame Clock

    #Joystick Initialization
    releaseCheck = 0
    joystickCount = pygame.joystick.get_count()
    Joystick = None
    for i in range(joystickCount):
        Joystick = pygame.joystick.Joystick(i)
        Joystick.init()

def end_pygame_runtime():
    global screenX
    global screenY
    global screen
    global font
    global mainClock
    global pyManXLayer
    global Joystick
    global releaseCheck

    pygame.quit()
    del screenX
    del screenY
    del screen
    del font
    del mainClock
    del Joystick
    del releaseCheck
    if (pyManXLayer):
        del pyManXLayer
    gc.collect()

#Load In-Game Overlay Assets
#Made a function so items can quickly be loaded and removed from memory
def load_ingame_assets():
    assets = [] #Asset Buffer
    #Audio
    assets.append(pygame.mixer.Sound(currentDir + "/Resources/Audio/open.wav"))                 #Menu Open       | 0
    assets.append(pygame.mixer.Sound(currentDir + "/Resources/Audio/back.wav"))                 #Back            | 1
    assets.append(pygame.mixer.Sound(currentDir + "/Resources/Audio/move.wav"))                 #Move Cursor     | 2
    #Graphics
    assets.append(pygame.image.load(currentDir + "/Resources/Images/home.bmp"))                 #House Icon      | 3
    assets.append(pygame.image.load(currentDir + "/Resources/Images/backArrow.bmp"))            #Back Icon       | 4
    assets.append(pygame.image.load(currentDir + "/Resources/Images/screenshot.bmp"))           #Camera Icon     | 5
    assets.append(pygame.image.load(currentDir + "/Resources/Images/check.bmp"))                #Check Icon      | 6
    assets.append(pygame.image.load(currentDir + "/Resources/Images/cross-round.bmp"))          #Cross Icon      | 7
    #Screenshot
    assets.append(pygame.image.load(currentDir + "/Resources/Temp/Temp.bmp"))                   #Temp Screenshot | 8
    return assets #Return the Asset Buffer

def load_notification_assets(load_index = None):
    assets = [] #Asset Buffer
    if(load_index == 0): #Achievement
        assets.append(pygame.mixer.Sound(currentDir + "/Resources/Audio/achievement.wav"))          #Audio | 0
        assets.append(pygame.image.load(currentDir + "/Resources/Images/trophy.bmp"))               #Icon  | 1
        assets.append("Trophy:")                                                                    #Text  | 2
    elif(load_index == 1): #Controller Status
        assets.append(pygame.mixer.Sound(currentDir + "/Resources/Audio/notification.wav"))         #Audio | 0
        assets.append(pygame.image.load(currentDir + "/Resources/Images/controller.bmp"))           #Icon  | 1
        assets.append("Controller:")                                                                #Text  | 2
    elif(load_index == 2): #Network Status
        assets.append(pygame.mixer.Sound(currentDir + "/Resources/Audio/notification.wav"))         #Audio | 0
        assets.append(pygame.image.load(currentDir + "/Resources/Images/controller.bmp"))           #Icon  | 1
        assets.append("Network:")                                                                   #Text  | 2
    elif(load_index == 3): #Screenshot
        assets.append(pygame.mixer.Sound(currentDir + "/Resources/Audio/notification.wav"))         #Audio | 0
        assets.append(pygame.image.load(currentDir + "/Resources/Temp/Temp.bmp"))                   #Icon  | 1
        assets.append("Screenshot:")                                                                #Text  | 2
    return assets #Return the Asset Buffer

#Draw Text on surface with color and x + y coordinates
def draw_text(text, font, color, surface, x, y, center = 0):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x - (center * (textrect.width/2)), y)
    surface.blit(textobj, textrect)

#Render Menu Selection based on index location
def menu_selector(menuLocation, buttonList, menuContents):
    for index, button in enumerate(buttonList):
        if(index != menuLocation):
            continue
        else:
            pygame.draw.circle(screen, cursorColor, (button.x + (button.width/2), button.y + (button.height/2)), (button.height/2) + 4, width=4)
            draw_text(menuContents[menuLocation], font, cursorColor, screen, button.x + (button.width/2), button.y - (button.height/4), 1)

def get_user_input(soundFX, i, indexLimit):
    global releaseCheck
    global Joystick

    buttonPressed = False

    #GAMEPAD INPUT
    if (Joystick != None):
        if Joystick.get_axis(0) > 0.2 and releaseCheck == 0:
            releaseCheck = 1
            pygame.mixer.Sound.play(soundFX)
            i = i + 1
        elif Joystick.get_axis(0) < -0.2 and releaseCheck == 0:
            releaseCheck = 1
            pygame.mixer.Sound.play(soundFX)
            i = i - 1
        elif Joystick.get_axis(0) < 0.2 and Joystick.get_axis(0) > -0.2 and Joystick.get_button(0) == 0:
            releaseCheck = 0

        if Joystick.get_button(0) == 1 and releaseCheck == 0:
            releaseCheck = 1
            buttonPressed = True

    for event in pygame.event.get():
        #KEYBOARD INPUT
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                pygame.mixer.Sound.play(soundFX)
                i = i + 1
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                pygame.mixer.Sound.play(soundFX)
                i = i - 1
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                buttonPressed = True

    if (i > indexLimit):
        i = 0
    elif (i < 0):
        i = indexLimit
    
    return i, not buttonPressed
    
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------

#Rendering Functions
#The following functions are for rendering menus to the display and can be used externally
#Render Screenshot Management UI
def save_screenshot(managePygame = True, AssetList = None):
    isRunning = True
    indexLocation = 0

    if managePygame:
        init_pygame_runtime(0)
        AssetList = load_ingame_assets()

    while(isRunning):
        screen.fill((0, 0, 0, 128)) #Updates Background Changes
        screenshot_surface = pygame.draw.rect(screen, primaryColor, (screenX/4, screenY/10, screenX/2, screenY/2))
        screen.blit(pygame.transform.scale(AssetList[8], (int(screenshot_surface.width), int(screenshot_surface.height))), (screenshot_surface.x, screenshot_surface.y))
        button_1 = pygame.draw.circle(screen, primaryColor, (screenX/3, 6*(screenY/7.25)), screenY/8)
        screen.blit(pygame.transform.scale(AssetList[6], (int(button_1.width/1.5), int(button_1.height/1.5))), (button_1.x + button_1.width/6, button_1.y + button_1.height/6))
        button_2 = pygame.draw.circle(screen, primaryColor, (screenX/3 + (screenX/3), 6*(screenY/7.25)), screenY/8)
        screen.blit(pygame.transform.scale(AssetList[7], (int(button_2.width/1.5), int(button_2.height/1.5))), (button_2.x + button_2.width/6, button_2.y + button_2.height/6))

        #Update Screen
        indexLocation, isRunning = get_user_input(AssetList[2], indexLocation, 1)
        menu_selector(indexLocation, [button_1, button_2], ["Save", "Cancel"])
        try:
            pyManXLayer.updateLayer()
        except:
            pygame.display.update()
        mainClock.tick(60)

    if indexLocation == 0:
        # sf.save_temp_screenshot()
        os.popen("python3 notification.py 3 Saved!") #This is a little inefficient but it works 

    #Clear Display and Unload Assets
    if managePygame:
        del AssetList #Unload Assets
        end_pygame_runtime() #Close pygame surfaces
    
    return indexLocation

#Render The In-Game Overlay and Get User Input
def ingame_overlay_main(gameCurrentlyRunning = False):
    isRunning = True
    init_pygame_runtime(0)
    AssetList = load_ingame_assets()
    ButtonList = None
    ButtonItems = None
    indexLocation = 0

    if (gameCurrentlyRunning):
        ButtonItems = ["Return to Game", "Home Menu", "Save Screenshot"]
    else:
        ButtonItems = ["Return", "Save Screenshot"]

    #Asset Index Values:
    #Menu Open   | Audio | i == 0
    #Back        | Audio | i == 1
    #Move Cursor | Audio | i == 2
    #House Icon  | Image | i == 3
    #Back Icon   | Image | i == 4
    #Camera Icon | Image | i == 5
    #Check Icon  | Image | i == 6
    #Cross Icon  | Image | i == 7

    pygame.mixer.Sound.play(AssetList[0])
    while(isRunning):
        screen.fill((0, 0, 0, 128)) #Updates Background Changes
        #Menu Buttons
        if (gameCurrentlyRunning):
            #Back Button
            button_1 = pygame.draw.circle(screen, primaryColor, (screenX/6, screenY/2), screenY/6)
            screen.blit(pygame.transform.scale(AssetList[4], (int(screenY/5), int(screenY/5))), (button_1.x + screenY/15, button_1.y + screenY/15))
            #Home Button
            button_2 = pygame.draw.circle(screen, primaryColor, (screenX/6 + (screenX/3), screenY/2), screenY/6)
            screen.blit(pygame.transform.scale(AssetList[3], (int(screenY/5), int(screenY/5))), (button_2.x + screenY/15, button_2.y + screenY/15))
            #Screenshot Button
            button_3 = pygame.draw.circle(screen, primaryColor, (screenX/6 + 2*(screenX/3), screenY/2), screenY/6)
            screen.blit(pygame.transform.scale(AssetList[5], (int(screenY/5), int(screenY/6))), (button_3.x + screenY/15, button_3.y + screenY/13))
            ButtonList = [button_1, button_2, button_3]
        else:
            #Back Button
            button_1 = pygame.draw.circle(screen, primaryColor, (screenX/3, screenY/2), screenY/6)
            screen.blit(pygame.transform.scale(AssetList[4], (int(screenY/5), int(screenY/5))), (button_1.x + screenY/15, button_1.y + screenY/15))
            #Screenshot Button
            button_2 = pygame.draw.circle(screen, primaryColor, (screenX/3 + screenX/3, screenY/2), screenY/6)
            screen.blit(pygame.transform.scale(AssetList[5], (int(screenY/5), int(screenY/6))), (button_2.x + screenY/15, button_2.y + screenY/13))
            ButtonList = [button_1, button_2]

        #Update Screen
        indexLocation, isRunning = get_user_input(AssetList[2], indexLocation, len(ButtonList) - 1)
        menu_selector(indexLocation, ButtonList, ButtonItems)
        if (gameCurrentlyRunning):
            if not isRunning and indexLocation == 2:
                save_screenshot(False, AssetList)
                init_pygame_runtime(0)
                isRunning = True
        else:
            if not isRunning and indexLocation == 1:
                save_screenshot(False, AssetList)
                init_pygame_runtime(0)
                isRunning = True
        try:
            pyManXLayer.updateLayer()
        except:
            pygame.display.update()
        mainClock.tick(60)

    #Clear Display and Unload Assets
    del AssetList #Unload Assets
    del ButtonList
    del ButtonItems
    end_pygame_runtime() #Close pygame surfaces
    return indexLocation

#Display a Notification
#Functionally, the user cannot interact with these. They are mainly for relaying info to the user.
#This function is awesome but will need to be run on another thread as it needs to wait for pygame
#to finish closing before it can return anything.

#Notification Type Index Values:
#Achievement | i == 0
#Controller  | i == 1
#Wireless    | i == 2

def send_system_notification(notificationType, notificationText):
    isRunning = True
    init_pygame_runtime(1)
    AssetList = load_notification_assets(notificationType) #Change to Notification Icon List
    notificationWidth = screenX/4.25 #Width can be modified as needed
    notificationHeight = screenY/10 #Height can be modified as needed
    renderOffset = -1 * notificationWidth
    runtime = 0

    #Asset Index Values:
    #Audio | i == 0
    #Image | i == 1
    #Text  | i == 2

    icon = pygame.transform.scale(AssetList[1], (int(notificationHeight), int(notificationHeight)))

    pygame.mixer.Sound.play(AssetList[0])
    while(isRunning):
        #Draw Notification Box
        screen.fill(0) #Updates Background Changes
        notificationBox = pygame.draw.rect(screen, primaryColor, (screenX - notificationWidth - renderOffset, notificationHeight * 1.5, notificationWidth, notificationHeight))
        pygame.draw.rect(screen, cursorColor, (screenX - notificationWidth - renderOffset, notificationHeight * 1.5, notificationWidth/26, notificationHeight))

        #Notification Content
        screen.blit(icon, (notificationBox.x + notificationWidth/26, notificationBox.y))
        draw_text(AssetList[2], font, (255,255,255), screen, notificationBox.x + notificationWidth/3, notificationBox.y + notificationHeight/6)
        draw_text(notificationText, font, (255,255,255), screen, notificationBox.x + notificationWidth/3, notificationBox.y + notificationHeight/2)

        #Update Screen
        try:
            pyManXLayer.updateLayer()
        except:
            pygame.display.update()
        mainClock.tick(60)
        if(runtime >= 325):
            isRunning = False
        elif(runtime >= 300):
            if (-1 * renderOffset < notificationWidth):
                renderOffset = renderOffset - notificationWidth/24
            runtime = runtime + 1
        else:
            if (renderOffset < 0):
                renderOffset = renderOffset + notificationWidth/24
            runtime = runtime + 1
    
    #Clear Display and Unload Assets
    del AssetList #Unload Assets
    end_pygame_runtime() #Close pygame surfaces
    return

#Display a Notification
#Functionally, the user cannot interact with these. They are mainly for relaying info to the user.
#This function is awesome but will need to be run on another thread as it needs to wait for pygame
#to finish closing before it can return anything.
def send_custom_notification(notificationText):
    isRunning = True
    init_pygame_runtime(1)
    notificationSound = pygame.mixer.Sound(currentDir + "/Resources/Audio/notification.wav")
    notificationWidth = screenX/4.25 #Width can be modified as needed
    notificationHeight = screenY/10 #Height can be modified as needed
    renderOffset = -1 * notificationWidth
    runtime = 0

    pygame.mixer.Sound.play(notificationSound)
    while(isRunning):
        #Draw Notification Box
        screen.fill(0) #Updates Background Changes
        notificationBox = pygame.draw.rect(screen, primaryColor, (screenX - notificationWidth - renderOffset, notificationHeight * 1.5, notificationWidth, notificationHeight))
        pygame.draw.rect(screen, cursorColor, (screenX - notificationWidth - renderOffset, notificationHeight * 1.5, notificationWidth/26, notificationHeight))

        #Notification Content
        draw_text(notificationText, font, (255,255,255), screen, notificationBox.x + notificationWidth/20, notificationBox.y + notificationHeight/3)

        #Update Screen
        try:
            pyManXLayer.updateLayer()
        except:
            pygame.display.update()
        mainClock.tick(60)
        if(runtime >= 325):
            isRunning = False
        elif(runtime >= 300):
            if (-1 * renderOffset < notificationWidth):
                renderOffset = renderOffset - notificationWidth/24
            runtime = runtime + 1
        else:
            if (renderOffset < 0):
                renderOffset = renderOffset + notificationWidth/24
            runtime = runtime + 1
    
    #Clear Display and Unload Assets
    del notificationSound #Unload Assets
    end_pygame_runtime() #Close pygame surfaces
    return

#Test Functions
if __name__ == '__main__':
    send_system_notification(0, "Close the Game") #Achievement
    send_system_notification(1, "Connected") #Controller Update
    send_custom_notification("I'm Listening") #General System Notification
    print(ingame_overlay_main(True))