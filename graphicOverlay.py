import pygame, os, gc
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

def end_pygame_runtime():
    global screenX
    global screenY
    global screen
    global font
    global mainClock
    global pyManXLayer

    pygame.quit()
    del screenX
    del screenY
    del screen
    del font
    del mainClock
    if (pyManXLayer):
        del pyManXLayer
    gc.collect()

#Load In-Game Overlay Assets
#Made a function so items can quickly be loaded and removed from memory
def load_ingame_assets():
    assets = [] #Asset Buffer
    #Audio
    assets.append(pygame.mixer.Sound(currentDir + "/Resources/Audio/open.wav"))                 #Menu Open    | 0
    assets.append(pygame.mixer.Sound(currentDir + "/Resources/Audio/back.wav"))                 #Back         | 1
    assets.append(pygame.mixer.Sound(currentDir + "/Resources/Audio/move.wav"))                 #Move Cursor  | 2
    #Graphics
    assets.append(pygame.image.load(currentDir + "/Resources/Images/home.bmp"))                 #House Icon   | 3
    assets.append(pygame.image.load(currentDir + "/Resources/Images/backArrow.bmp"))            #Back Icon    | 4
    assets.append(pygame.image.load(currentDir + "/Resources/Images/screenshot.bmp"))           #Camera Icon  | 5
    assets.append(pygame.image.load(currentDir + "/Resources/Images/check.bmp"))                #Check Icon   | 6
    assets.append(pygame.image.load(currentDir + "/Resources/Images/cross-round.bmp"))          #Cross Icon   | 7
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
    return assets #Return the Asset Buffer

#Draw Text on surface with color and x + y coordinates
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------

#Rendering Functions
#The following functions are for rendering menus to the display and can be used externally
#Render The In-Game Overlay and Get User Input
def ingame_overlay_main():
    isRunning = True
    init_pygame_runtime(0)
    AssetList = load_ingame_assets()
    i = 0

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
        screen.fill(0) #Updates Background Changes
        #Menu Buttons
        #Back Button
        button_1 = pygame.draw.circle(screen, primaryColor, (screenX/6, screenY/2), screenY/6)
        screen.blit(pygame.transform.scale(AssetList[4], (int(screenY/5), int(screenY/5))), (button_1.x + screenY/15, button_1.y + screenY/15))
        #Home Button
        button_2 = pygame.draw.circle(screen, primaryColor, (screenX/6 + (screenX/3), screenY/2), screenY/6)
        screen.blit(pygame.transform.scale(AssetList[3], (int(screenY/5), int(screenY/5))), (button_2.x + screenY/15, button_2.y + screenY/15))
        #Screenshot Button
        button_3 = pygame.draw.circle(screen, primaryColor, (screenX/6 + 2*(screenX/3), screenY/2), screenY/6)
        screen.blit(pygame.transform.scale(AssetList[5], (int(screenY/5), int(screenY/6))), (button_3.x + screenY/15, button_3.y + screenY/13))
        #Update Screen
        try:
            pyManXLayer.updateLayer()
        except:
            pygame.display.update()
        mainClock.tick(60)
        if(i >= 500):
            isRunning = 0
        else:
            i = i + 1

    #Clear Display and Unload Assets
    del AssetList #Unload Assets
    end_pygame_runtime() #Close pygame surfaces
    return

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
        screen.blit(icon, (notificationBox.x + notificationWidth/16, notificationBox.y))
        draw_text(AssetList[2], font, (255,255,255), screen, notificationBox.x + notificationWidth/3, notificationBox.y + notificationHeight/6)
        draw_text(notificationText, font, (255,255,255), screen, notificationBox.x + notificationWidth/3, notificationBox.y + notificationHeight/2)

        #Update Screen
        try:
            pyManXLayer.updateLayer()
        except:
            pygame.display.update()
        mainClock.tick(60)
        if(runtime >= 375):
            isRunning = 0
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
        if(runtime >= 375):
            isRunning = 0
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
    send_system_notification(0, "Climb a Mountain") #Achievement
    send_system_notification(0, "Close the Game")
    send_system_notification(1, "Connected") #Controller Update
    send_system_notification(1, "Disconnected")
    send_custom_notification("Just saying hi") #General System Notification
    ingame_overlay_main()