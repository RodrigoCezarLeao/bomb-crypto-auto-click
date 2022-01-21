import json
import pyautogui as pt
from time import sleep, time, gmtime
from threading import Timer
from os import system, startfile
import keyboard
import pymsgbox

def wait(seconds):
    sleep(seconds)

def openPath(path, timeToWait):
    try:
        startfile(f'"{path}"')
        wait(timeToWait)
    except:
        raise Exception(f"Erro ao abrir arquivo '{path}'")

def click(coord, timeToWait):
    try:
        x, y = coord
        pt.moveTo(x, y, 0)
        pt.click()
        wait(timeToWait)
    except:
        raise Exception(f"Erro ao realizar o clique em coordenada '({x},{y})' da tela")

def write(text, timeToWait):
    try:
        keyboard.write(text)
        wait(timeToWait)
    except:
        raise Exception(f"Erro ao digitar texto '{text}' no campo desejado")

def pressKey(keyCombination, timeToWait):
    try:
        keyboard.press(keyCombination)
        wait(timeToWait)
    except:
        raise Exception(f"Erro ao pressionar tecla(s) '{keyCombination}'")





def totalExecutionTime(t0):
    timeObj = gmtime(time() - t0)
    return f"\nTempo total de execução do bot: {(timeObj.tm_yday - 1):02d}:{timeObj.tm_hour:02d}:{timeObj.tm_min:02d}:{timeObj.tm_sec:02d}\n\n"

def actionExecutionTime(t1, actionName, actionRep):
    timeObj = gmtime(time() - t1)
    action = config["remarks"][actionName]
    actionOneTimeInSec = calculateFullTimeOfAStep(actionName)
    actionOneTimeInSecObj = gmtime(actionOneTimeInSec)
    actionFullTimeInSec = calculateFullTimeOfAStep(actionName) * actionRep
    actionTimeObj = gmtime(actionFullTimeInSec)

    str1 = f"Tempo estimado (sem pausas) de execução de '{action}' (x1): {(actionOneTimeInSecObj.tm_yday - 1):02d}:{actionOneTimeInSecObj.tm_hour:02d}:{actionOneTimeInSecObj.tm_min:02d}:{actionOneTimeInSecObj.tm_sec:02d}\n"
    str2 = f"Quantidade de repetições: {actionRep}\n"
    str3 = ""
    str4 = f"Tempo real passado da ação atual até o momento: {(timeObj.tm_yday - 1):02d}:{timeObj.tm_hour:02d}:{timeObj.tm_min:02d}:{timeObj.tm_sec:02d}\n"

    if(actionRep > 1):
        str3 = f"Tempo estimado (sem pausas) total de execução de '{action}' (x{actionRep}): {(actionTimeObj.tm_yday - 1):02d}:{actionTimeObj.tm_hour:02d}:{actionTimeObj.tm_min:02d}:{actionTimeObj.tm_sec:02d}\n"
        

    return f"{str1}{str2}{str3}{str4}"

def calculateFullTimeOfAStep(actionName):
    totalSeconds = 0

    try:
        stepSet = config[resolution][actionName]
        for step in stepSet:
            try:
                totalSeconds += float(step["waitTimeAfter"])
            except:
                raise Exception("Passo '{step}' não possui valor válido para tempo de espera pós execução")
    except:
        raise Exception("Ação '{actionName}' não cadastrada no 'config'")
    
    return totalSeconds


def reportInfo(actionName, t0, t1, actionRep):
    system("cls")
    str1 = totalExecutionTime(t0)
    str2 = actionExecutionTime(t1, actionName, actionRep)    
    message = f"Bombcrypto Autoclick Bot\n{str1}\n{str2}"
    #pymsgbox.alert(message)
    print(message)

def executeAction(actionName, config, t0, t1, actionRep, metamaskPassword):
    global pause    
    if(actionName in config):
        action = config[actionName]

        for step in action:
            if(pause):
                checkPause()

            reportInfo(actionName, t0, t1, actionRep)

            type = step["type"]
            waitTimeAfter = step["waitTimeAfter"]
            value = step["value"]
            remark = step["remark"]
            
            f = None
            if type == "click":
                f = click
            elif type == "openPath":
                f = openPath
            elif type == "write":
                if(value == "password"):
                    value = metamaskPassword
                f = write                
            elif type == "pressKey":
                f = pressKey

            f(value, waitTimeAfter)


def schema(metamaskPassword):
    t0 = time()    
    schema = config["schema"]    

    for actionSet in schema:
        rep = int(actionSet["rep"])
        
        i = 0
        while(i < rep):
            for action in actionSet["actions"]:                
                actionName = action["action"]
                actionRep = action["rep"]

                #Time of the full action execution besides time of each repetition of the same action
                t1 = time()

                j = 0
                while(j < actionRep):                    
                    executeAction(actionName, config[resolution], t0, t1, actionRep, metamaskPassword)
                    j += 1


            i += 1
        

def checkPause():
    global pause
    system("cls")    
    input("\n\nBot pausado.. pressione a tecla 'enter' para continuar")    
    pause = False

def pauseGame():
    global pause
    print("\n\nPausando bot no próximo comando..\nPor favor, espere..")
    pause = not pause



pause = False
fp = open('config - v2.0.json')
config = json.load(fp)
resolution = config["resolution"]
keyboard.add_hotkey('ctrl+f1', pauseGame)

metamaskPassword = pymsgbox.password('Insira sua senha da metamask, caso não esteja no arquivo config', 'Senha')

schema(metamaskPassword)
