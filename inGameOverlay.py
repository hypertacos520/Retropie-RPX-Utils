import pydispmanx #Literally can't believe this exists I'm so stoked
import pygame
import time 
import sys
import os
from datetime import datetime
from pygame.locals import *
from PIL import Image

#pygame.init()

#input screen dimensions for menu to display correctly
#screenX = 1280 #640
#screenY = 720 #400
screenX, screenY = pydispmanx.getDisplaySize()

highlightColor = (16, 174, 190)
highlightTransparency = 255

menuSelection = 0 #Default action is to resume processes
currentDirectory = os.path.dirname(os.path.realpath(__file__))
mainClock = pygame.time.Clock()
pygame.init()
#Joystick Initialization
joystick_count = pygame.joystick.get_count()
for i in range(joystick_count):
    Joystick = pygame.joystick.Joystick(i)
    Joystick.init()
    JoystickDeadzone = Joystick.get_axis(i)
pygame.display.set_caption('In Game Overlay')
testlayer = pydispmanx.dispmanxLayer(9);
time.sleep(0.5)
screen = pygame.image.frombuffer(testlayer, testlayer.size, 'RGBA')#pygame.display.set_mode((screenX, screenY),0,32)
time.sleep(0.5)
initalOpen = pygame.mixer.Sound(currentDirectory + "/Resources/Audio/Jig 1.wav")
Back = pygame.mixer.Sound(currentDirectory + "/Resources/Audio/Interface Click 4.wav")
updown = pygame.mixer.Sound(currentDirectory + "/Resources/Audio/Interface Click 1.wav")
homeIcon = pygame.transform.scale(pygame.image.load(currentDirectory + "/Resources/Images/home.bmp"), (int(screenY/5), int(screenY/5)))
backIcon = pygame.transform.scale(pygame.image.load(currentDirectory + "/Resources/Images/backArrow.bmp"), (int(screenY/5), int(screenY/5)))
screenshotIcon = pygame.transform.scale(pygame.image.load(currentDirectory + "/Resources/Images/screenshot.bmp"), (int(screenY/5), int(screenY/6)))
checkIcon = pygame.transform.scale(pygame.image.load(currentDirectory + "/Resources/Images/check.bmp"), (int(screenY/5), int(screenY/5)))
crossIcon = pygame.transform.scale(pygame.image.load(currentDirectory + "/Resources/Images/cross-round.bmp"), (int(screenY/5), int(screenY/5)))
file_in = currentDirectory + "/Resources/Temp/bg.png"
img = Image.open(file_in)
file_out = currentDirectory + "/Resources/Temp/bg.bmp"
img.save(file_out)
bg = pygame.transform.scale(pygame.image.load(currentDirectory + "/Resources/Temp/bg.bmp"), (screenX, screenY))
dark = pygame.Surface((bg.get_width(), bg.get_height()), flags=pygame.SRCALPHA)
dark.fill((100, 100, 100, 0))
bg.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

font = pygame.font.SysFont(None, int(screenX/30))
releaseCheck = 0

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False

def menu_selector(menuLocation):
    if menuLocation == 0:
        pygame.draw.circle(screen, highlightColor, (screenX/6, screenY/2), (screenY/6) + 4, width=4)
        #pygame.draw.circle(screen, (255,255,255), (screenX/4, screenY/2), (screenY/5) + 4, width=4)
        draw_text('Return To Game', font, highlightColor, screen, screenX/12, screenY/4)
        #pygame.draw.rect(screen, (0, 100, 255), (50, 100, 200, 50), 3)  # width = 3
    if menuLocation == 1:
        pygame.draw.circle(screen, highlightColor, (screenX/6 + (screenX/3), screenY/2), (screenY/6) + 4, width=4)
        #pygame.draw.circle(screen, (255,255,255), (screenX/4 + 2*(screenX/4), screenY/2), (screenY/5) + 4, width=4)
        draw_text('Home Menu', font, highlightColor, screen, 5*(screenX/12) + screenX/48, screenY/4)
        #pygame.draw.rect(screen, (0, 100, 255), (50, 200, 200, 50), 3)  # width = 3
    if menuLocation == 2:
        pygame.draw.circle(screen, highlightColor, (screenX/6 + 2*(screenX/3), screenY/2), (screenY/6) + 4, width=4)
        #pygame.draw.circle(screen, (255,255,255), (screenX/4 + 2*(screenX/4), screenY/2), (screenY/5) + 4, width=4)
        draw_text('Save Screenshot', font, highlightColor, screen, 9*(screenX/12), screenY/4)
        #pygame.draw.rect(screen, (0, 100, 255), (50, 200, 200, 50), 3)  # width = 3

def main_menu():
    menuLocation = 0
    global menuSelection
    global releaseCheck
    running = 1

    try:
        while True:

            screen.fill((0,0,0))
            screen.blit(bg, (0, 0))
            #pygame.draw.rect(screen, (0,0,0), (screenX, screenY, screenX, screenY))

            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.draw.circle(screen, (81, 81, 81), (screenX/6, screenY/2), screenY/6)
            screen.blit(backIcon, (button_1.x + screenY/15, button_1.y + screenY/15))
            button_2 = pygame.draw.circle(screen, (81, 81, 81), (screenX/6 + (screenX/3), screenY/2), screenY/6)
            screen.blit(homeIcon, (button_2.x + screenY/15, button_2.y + screenY/15))
            button_3 = pygame.draw.circle(screen, (81, 81, 81), (screenX/6 + 2*(screenX/3), screenY/2), screenY/6)
            screen.blit(screenshotIcon, (button_3.x + screenY/15, button_3.y + screenY/13))
            menu_selector(menuLocation)
            #pygame.draw.rect(screen, (255, 0, 0), button_1)
            #pygame.draw.rect(screen, (255, 0, 0),menu_selector(menuLocation) button_2)

            click = False
            #GAMEPAD INPUT
            if joystick_count > 0:
                if Joystick.get_axis(0) < JoystickDeadzone and releaseCheck == 0:
                    releaseCheck = 1
                    pygame.mixer.Sound.play(updown)
                    menuLocation = menuLocation - 1
                elif Joystick.get_axis(0) > JoystickDeadzone and releaseCheck == 0:
                    releaseCheck = 1
                    pygame.mixer.Sound.play(updown)
                    menuLocation = menuLocation + 1
                elif Joystick.get_axis(0) == JoystickDeadzone and Joystick.get_button(0) == 0:
                    releaseCheck = 0
                if Joystick.get_button(0) == 1 and releaseCheck == 0:
                    releaseCheck = 1
                    if menuLocation == 2:
                        running = 0
                        screenshot()
                    else:
                        pygame.quit()
                        #sys.exit()
                        menuSelection = menuLocation
                        return menuLocation
                    pygame.quit()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    #sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        #sys.exit()
                #KEYBOARD INPUT
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        pygame.mixer.Sound.play(updown)
                        menuLocation = menuLocation + 1
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        pygame.mixer.Sound.play(updown)
                        menuLocation = menuLocation - 1
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        if menuLocation == 2:
                            running = 0
                            screenshot()
                        else:
                            pygame.quit()
                            #sys.exit()
                            menuSelection = menuLocation
                            return menuLocation
                        pygame.quit()
                #OTHER BUTTON INPUTS
                if event.type == KEYDOWN:
                    if event.key == K_c:
                        pygame.quit()
                        #sys.exit()
                        return menuLocation
                if event.type == KEYDOWN:
                    if event.key == K_0:
                        pygame.mixer.Sound.play(Back)
                        pygame.quit()
                        #sys.exit()
                        return 0
                if event.type == MOUSEBUTTONDOWN:
                    if button_1.collidepoint(mx, my) and menuLocation != 0:
                        menuLocation = 0
                        pygame.mixer.Sound.play(updown)
                    elif button_2.collidepoint(mx, my) and menuLocation != 1:
                        menuLocation = 1
                        pygame.mixer.Sound.play(updown)
                    elif button_3.collidepoint(mx, my) and menuLocation != 2:
                        menuLocation = 2
                        pygame.mixer.Sound.play(updown)
                    elif button_3.collidepoint(mx, my) and menuLocation == 2:
                        running = 0
                        #screenshot()
                    elif button_2.collidepoint(mx, my) and menuLocation == 1:
                        return 1
                    elif button_1.collidepoint(mx, my) and menuLocation == 0:
                        return 0

                    #if event.button == 1:
                    #    click = True

            if menuLocation > 2:
                menuLocation = 0
            if menuLocation < 0:
                menuLocation = 2
            

            #pygame.display.update()
            testlayer.updateLayer()
            mainClock.tick(60)
    except:
        pass

def screenshot_selector(screenshotLocation):
    if screenshotLocation == 0:
        pygame.draw.circle(screen, highlightColor, (screenX/3, 6*(screenY/8)), (screenY/6) + 4, width=4)
        #pygame.draw.circle(screen, (255,255,255), (screenX/4, screenY/2), (screenY/5) + 4, width=4)
        draw_text('Save', font, highlightColor, screen, screenX/6 + 1.75*(screenX/12), 4*(screenY/8))
        #pygame.draw.rect(screen, (0, 100, 255), (50, 100, 200, 50), 3)  # width = 3
    if screenshotLocation == 1:
        pygame.draw.circle(screen, highlightColor, (screenX/3 + (screenX/3), 6*(screenY/8)), (screenY/6) + 4, width=4)
        #pygame.draw.circle(screen, (255,255,255), (screenX/4 + 2*(screenX/4), screenY/2), (screenY/5) + 4, width=4)
        draw_text("Don't Save", font, highlightColor, screen, 3*(screenX/6) + 1.3*(screenX/12), 4*(screenY/8))
        #pygame.draw.rect(screen, (0, 100, 255), (50, 200, 200, 50), 3)  # width = 3

def screenshot():
    bg = pygame.transform.scale(pygame.image.load(currentDirectory + "/Resources/Temp/bg.bmp"), (screenX, screenY))
    screenshotLocation = 0
    file_in = currentDirectory + "/Resources/Temp/bg.png"
    img = Image.open(file_in)
    global releaseCheck

    try:
        running = True
        while running:
            mx, my = pygame.mouse.get_pos()
            screen.fill((0,0,0))
            screen.blit(bg, (0, 0))
            
            button_1 = pygame.draw.circle(screen, (81, 81, 81), (screenX/3, 6*(screenY/8)), screenY/6)
            screen.blit(checkIcon, (button_1.x + screenY/15, button_1.y + screenY/15))
            button_2 = pygame.draw.circle(screen, (81, 81, 81), (screenX/3 + (screenX/3), 6*(screenY/8)), screenY/6)
            screen.blit(crossIcon, (button_2.x + screenY/15, button_2.y + screenY/15))

            screenshot_selector(screenshotLocation)

            #GAMEPAD INPUT
            if joystick_count > 0:
                if Joystick.get_axis(0) < JoystickDeadzone and releaseCheck == 0:
                    releaseCheck = 1
                    pygame.mixer.Sound.play(updown)
                    screenshotLocation = screenshotLocation - 1
                elif Joystick.get_axis(0) > JoystickDeadzone and releaseCheck == 0:
                    releaseCheck = 1
                    pygame.mixer.Sound.play(updown)
                    screenshotLocation = screenshotLocation + 1
                elif Joystick.get_axis(0) == JoystickDeadzone and Joystick.get_button(0) == 0:
                    releaseCheck = 0
                if Joystick.get_button(0) == 1 and releaseCheck == 0:
                    releaseCheck = 1
                    if screenshotLocation == 0:
                        running = False
                        file_out = currentDirectory + "/../screenshots/" + str(datetime.now()) + ".png"
                        img.save(file_out)
                        print("Saving to " + file_out)
                        finishedSaving()
                    else:
                        main_menu()
            #draw_text('Save The Current Image?', font, (255, 0, 0), screen, screenX/2, screenY/2)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            #KEYBOARD INPUT
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        pygame.mixer.Sound.play(updown)
                        screenshotLocation = screenshotLocation + 1
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        pygame.mixer.Sound.play(updown)
                        screenshotLocation = screenshotLocation - 1
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        if screenshotLocation == 0:
                            running = False
                            file_out = currentDirectory + "/../screenshots/" + str(datetime.now()) + ".png"
                            img.save(file_out)
                            print("Saving to " + file_out)
                            finishedSaving()
                        else:
                            main_menu()

                #GAMEPAD INPUT
                #if running == 1:
                #    if Joystick.get_axis(0) < JoystickDeadzone:
                #        pygame.mixer.Sound.play(updown)
                #        screenshotLocation = screenshotLocation - 1
                #    elif Joystick.get_axis(0) > JoystickDeadzone:
                #        pygame.mixer.Sound.play(updown)
                #        screenshotLocation = screenshotLocation + 1
                #    if Joystick.get_button(0) == 1:
                #        if screenshotLocation == 0:
                #            running = False
                #            file_out = currentDirectory + "/../screenshots/" + str(datetime.now()) + ".png"
                #            img.save(file_out)
                #            finishedSaving()
                #        else:
                #            main_menu()
                #OTHER BUTTON INPUTS
                if event.type == KEYDOWN:
                    if event.key == K_c:
                        pygame.quit()
                        #sys.exit()
                        return 2
                if event.type == KEYDOWN:
                    if event.key == K_0:
                        pygame.mixer.Sound.play(Back)
                        pygame.quit()
                        #sys.exit()
                        return 0
                if event.type == MOUSEBUTTONDOWN:
                    if button_1.collidepoint(mx, my) and screenshotLocation != 0:
                        screenshotLocation = 0
                        pygame.mixer.Sound.play(updown)
                    elif button_2.collidepoint(mx, my) and screenshotLocation != 1:
                        screenshotLocation = 1
                        pygame.mixer.Sound.play(updown)
                    elif button_2.collidepoint(mx, my) and screenshotLocation == 1:
                        main_menu()
                    elif button_1.collidepoint(mx, my) and screenshotLocation == 0:
                        running = False
                        file_out = currentDirectory + "/../screenshots/" + str(datetime.now()) + ".png"
                        print("Saving to " + file_out)
                        img.save(file_out)
                        finishedSaving()

            if screenshotLocation > 1:
                screenshotLocation = 0
            if screenshotLocation < 0:
                screenshotLocation = 1
            
            testlayer.updateLayer()
            mainClock.tick(60)
    except:
        pass

def finishedSaving():
    running = True
    while running:
        screen.fill((0,0,0))
        screen.blit(bg, (0, 0))

        draw_text('Image Saved!', font, (255, 0, 0), screen, (screenX/3 + screenX/10), screenY/2)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        testlayer.updateLayer()
        mainClock.tick(60)
        time.sleep(3)
        running = False
        main_menu()

pygame.mixer.Sound.play(initalOpen)
main_menu()
print(menuSelection)
#print(main_menu())
