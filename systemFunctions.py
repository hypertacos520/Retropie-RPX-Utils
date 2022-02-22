import subprocess, os, psutil, getpass
from datetime import datetime

#The process names in the following list will not be affected by the freeze, resume, and terminate functions
#This list may need modified based on newer retropie installations
necessaryProcesses = ['bash', 'pegasus-fe', 'ps', 'python3', 'sshd', 'systemd', '(sd-pam)', 'dbus-daemon', 'sudo', 'sftp-server']

#Determines if a given string is a real numerical value
def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

#Freezes all processes besides those in the necessaryProcesses list
def freeze_processes():
    processList = get_running_processes()
    for i in range(len(processList)):
        if i % 2 != 0:
            continue
        dontFreeze = 0
        for process in necessaryProcesses:
            if process == processList[i+1]:
                dontFreeze = 1
        if dontFreeze == 1:
            dontFreeze = 0
            continue
        os.kill(int(processList[i]), 19)#sends STOP signal
        dontFreeze = 0
        print('Process Frozen. ID: ' + str(processList[i]) + ' Name: ' + str(processList[i+1])) #Debug Statement

#Resumes all processes besides those in the necessaryProcesses list
def resume_processes():
    processList = get_running_processes()
    for i in range(len(processList)):
        if i % 2 != 0:
            continue
        dontFreeze = 0
        for process in necessaryProcesses:
            if process == processList[i+1]:
                dontFreeze = 1
        if dontFreeze == 1:
            dontFreeze = 0
            continue
        os.kill(int(processList[i]), 18)#sends CONT signal
        dontFreeze = 0
        print('Process Resumed. ID: ' + str(processList[i]) + ' Name: ' + str(processList[i+1])) #Debug Statement

#Terminates all processes besides those in the necessaryProcesses list
def terminate_processes():
    processList = get_running_processes()
    for i in range(len(processList)):
        if i % 2 != 0:
            continue
        dontFreeze = 0
        for process in necessaryProcesses:
            if process == processList[i+1]:
                dontFreeze = 1
        if dontFreeze == 1:
            dontFreeze = 0
            continue
        os.kill(int(processList[i]), 9)#sends KILL signal
        dontFreeze = 0
        print('Process Terminated. ID: ' + str(processList[i]) + ' Name: ' + str(processList[i+1])) #Debug Statement

#Returns a list of the currently running processes in the following form:
#pid1, pname1, pid2, pname2, pid3, pname3...
#This is the old implementation. If no issues are found in the new version this will be depricated
#Old implementation relies heavily on string processing and has a lot of potential for problems
def get_running_processes_old():
    string = subprocess.run(['ps', '-a'], stdout=subprocess.PIPE)
    li = list(str(string).split(" "))
    newLi = []
    for item in li:
        if item == '':
            continue
        else:
            newLi.append(item)
    evenNewerLi = []
    i = 0
    currentPos = 0
    for item in newLi:
        if is_integer(item):
            evenNewerLi.append(item)
            currentPos = currentPos + 1
            continue
        if currentPos == 3:
            evenNewerLi.append(item.replace('\\n', ''))
            currentPos = 0
            i = i + 1
            continue
        if currentPos > 0:
            currentPos = currentPos + 1
    finalList = []
    for item in evenNewerLi:
        finalList.append(item.replace("')", ""))
    return finalList

#Returns a list of the currently running processes in the following form:
#pid1, pname1, pid2, pname2, pid3, pname3...
def get_running_processes():
    username = getpass.getuser()
    runningProcesses = []
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            if (proc.username() == username):
                runningProcesses.append(proc.pid)
                runningProcesses.append(proc.name())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return runningProcesses


#Returns true if a game is active and false if there is not
def is_in_game():
    processList = get_running_processes()
    for i in range(len(processList)):
        if i % 2 != 0:
            continue
        j = 0
        for process in necessaryProcesses:
            if process == processList[i+1]:
                break
            elif j == len(necessaryProcesses) - 1:
                return True
            else:
                j = j + 1
    return False

#Returns True if a specified process with ID: pid is running and False if it is not
def is_process_active(pid):
    processList = get_running_processes()
    for i in range(len(processList)):
        if i % 2 != 0:
            continue
        if int(pid) == int(processList[i]):
            if processList[i+1].find('<defunct>') != -1:
                break
            else:
                return True
    return False

#Takes a screenshot using raspi2png
#Retropie has no window manager making this process dificult, hence the need for this function
#Save is a binary value that will save the image to 1 of 2 locations
#Save == 0 | /Resources/Temp/Temp.png
#Save == 1 | ../Screenshots/(datetime.now()).png
def take_screenshot(save):
    currentDirectory = os.path.dirname(os.path.realpath(__file__))
    if(save):
        saveLocation = currentDirectory + '../Screenshots/' + str(datetime.now()) + ".png"
    else:
        saveLocation = currentDirectory + '/Resources/Temp/Temp.png'
    print(subprocess.run(['raspi2png', '-p', saveLocation], stdout=subprocess.PIPE)) #print is for debug


#testing functions
if __name__ == '__main__':
    print("get_running_processes_old output:")
    print(get_running_processes_old())

    print("get_running_processes output:")
    print(get_running_processes())