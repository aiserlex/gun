import os
import math
import time
import win32api, win32con, win32gui

def drawSmile():
    
    x0 = 500
    y0 = 500

    t = 0
    while t <= 2*math.pi + 0.1:
        win32api.SetCursorPos((math.trunc(100*math.cos(t)+x0), math.trunc(100*math.sin(t)+y0)))
        if t == 0:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(.05)
        t += 2*math.pi/50 
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    
    t = 0
    while t <= 2*math.pi + 0.1:
        win32api.SetCursorPos((math.trunc(10*math.cos(t)+x0-50), math.trunc(10*math.sin(t)+y0-50)))
        if t == 0:            
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(.05)
        t += 2*math.pi/20 
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    
    t = 0
    while t <= 2*math.pi + 0.1:
        win32api.SetCursorPos((math.trunc(10*math.cos(t)+x0+50), math.trunc(10*math.sin(t)+y0-50)))
        if t == 0:            
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(.05)
        t += 2*math.pi/20 
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    t = math.pi/4
    while t <= 3*math.pi/4:
        win32api.SetCursorPos((math.trunc(100*math.cos(t)+x0), math.trunc(100*math.sin(t)+y0-50)))
        if t == math.pi/4:            
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(.05)
        t += 2*math.pi/50 
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)    

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    
if __name__ == '__main__':
    time.sleep(0.5)
    os.startfile(r'C:\Windows\system32\mspaint.exe', 'open')
    time.sleep(1)
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    print(top_windows)
    for i in top_windows:
        if "paint" in i[1].lower():
            win32gui.ShowWindow(i[0],5)
            win32gui.SetForegroundWindow(i[0])
            break    
    drawSmile()
