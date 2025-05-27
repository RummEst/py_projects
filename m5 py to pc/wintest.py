import pygetwindow as gw



def toggleReoWin():
    reoWin = gw.getWindowsWithTitle('Reolink')[0]
    print("Toggle reoWin")
    if reoWin.isMaximized:
        reoWin.minimize()
    elif not reoWin.isMaximized:
        reoWin.maximize()
    else:
        print("toggleReoWin() -> Error")




