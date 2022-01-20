import pyautogui as pt
import keyboard
import pymsgbox

def myfunc():
    pymsgbox.alert(pt.position(), "Coordenadas do Ponteiro do Mouse")

keyboard.add_hotkey('ctrl+f1', myfunc)
while(True):
    input()