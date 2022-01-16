#pip install pyautogui
#https://www.geeksforgeeks.org/mouse-keyboard-automation-using-python/

import json
import pyautogui as pt
from time import sleep, time, gmtime
from threading import Timer
from os import system

fp = open('config.json')
config = json.load(fp)

def allToDO(mode):
    #mode = 1 (WORK) | mode = 2 (REST)
    resolution = config["resolution"]
    sleepTime = config["clickOffsetToRequest"]
    mouseTravellingInterval = config["mouseTravellingInterval"]

    #Backward Button Click
    goBackX = config[resolution]["goBackwardButtonCood"]["x"]
    goBackY = config[resolution]["goBackwardButtonCood"]["y"]
    pt.moveTo(goBackX,goBackY, mouseTravellingInterval)
    pt.click()
    sleep(sleepTime)
    
    #Heroes Button Click
    heroesX = config[resolution]["heroesButtonCoord"]["x"]
    heroesY = config[resolution]["heroesButtonCoord"]["y"]
    pt.moveTo(heroesX,heroesY, mouseTravellingInterval)
    pt.click()
    sleep(sleepTime)
    
    #All Heroes to Work Button Click
    workAllX = config[resolution]["workAllHeroesCoord"]["x"]
    workAllY = config[resolution]["workAllHeroesCoord"]["y"]
    restAllX = config[resolution]["restAllHeroesCoord"]["x"]
    restAllY = config[resolution]["restAllHeroesCoord"]["y"]
    
    if(mode == 1):
        pt.moveTo(workAllX,workAllY, mouseTravellingInterval)
    elif(mode == 2):
        pt.moveTo(restAllX,restAllY, mouseTravellingInterval)
    pt.click()
    sleep(sleepTime)
    
    #Close Button Click
    closeHeroesX = config[resolution]["closeHeroesModalCoord"]["x"]
    closeHeroesY = config[resolution]["closeHeroesModalCoord"]["y"]
    pt.moveTo(closeHeroesX,closeHeroesY, mouseTravellingInterval)
    pt.click()
    sleep(sleepTime)
    
    #Treasure Hunt Mode Button Click
    treasureHuntX = config[resolution]["treasureHuntModeCoord"]["x"]
    treasureHuntY = config[resolution]["treasureHuntModeCoord"]["y"]
    pt.moveTo(treasureHuntX,treasureHuntY, mouseTravellingInterval)
    pt.click()
    sleep(sleepTime)



def keepMapOpened():
    resolution = config["resolution"]
    sleepTime = config["timeOffsetToOpenAndCloseChestModal"]
    mouseTravellingInterval = config["mouseTravellingInterval"]

    openX = config[resolution]["openChestModalCoord"]["x"]
    openY = config[resolution]["openChestModalCoord"]["y"]    

    closeX = config[resolution]["closeChestModalCoord"]["x"]
    closeY = config[resolution]["closeChestModalCoord"]["y"]
    
    pt.moveTo(openX,openY, mouseTravellingInterval)
    pt.click()
    sleep(sleepTime)

    pt.moveTo(closeX,closeY, mouseTravellingInterval)
    pt.click()
    sleep(sleepTime)


def printInfo(actionCode, timeDoing, totalTime, cont):
    system("cls")

    print(f"Atualização de Tela: {cont}")

    if(actionCode == 1):
        #Working
        jobPercentage = round((timeDoing / totalTime) * 100, 2)
        print(f"Modo Trabalho ({jobPercentage}%)")        
        timeDoingObj = gmtime(timeDoing)
        totalTimeObj = gmtime(totalTime)        
        print(f"Tempo = {timeDoingObj.tm_min}:{timeDoingObj.tm_sec} / {totalTimeObj.tm_min}:{totalTimeObj.tm_sec}")
    if(actionCode == 2):
        #Resting
        jobPercentage = round((timeDoing / totalTime) * 100, 2)
        print(f"Modo Descanso ({jobPercentage}%)")
        timeDoingObj = gmtime(timeDoing)
        totalTimeObj = gmtime(totalTime)
        print(f"Tempo = {timeDoingObj.tm_min}:{timeDoingObj.tm_sec} / {totalTimeObj.tm_min}:{totalTimeObj.tm_sec}")
    if(actionCode == 3):
        #Heroes to Work
        print("Acordar Heroes (Hora de Trabalhar!)")
    if(actionCode == 4):
        #Heroes to Rest
        print("Descansar Heroes (Hora de Dormir!)")


def hub(cont):        
    workTimeInSec = config["workTimeInSec"]
    restTimeInSec = config["restTimeInSec"]
    
    #Wake Up Them All
    cont += 1
    printInfo(3, None, None, cont)
    allToDO(1)

    #Keep game opened (WORKING)
    t0 = time()
    t1 = time()
    while(t1 - t0 < workTimeInSec):
        cont += 1
        printInfo(1, t1 - t0, workTimeInSec, cont)
        keepMapOpened()
        t1 = time()

    #Rest Them All
    cont += 1
    printInfo(4, None, None, cont)
    allToDO(2)
    

    #Keep game opened (RESTING)
    t0 = time()
    t1 = time()
    while(t1 - t0 < restTimeInSec):
        cont += 1
        printInfo(2, t1 - t0, restTimeInSec, cont)
        keepMapOpened()
        t1 = time()

    return cont


cont = 0
while(True):
    cont = hub(cont)