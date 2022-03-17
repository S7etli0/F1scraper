import time

def progressload(loadtab):
    bars = 12
    while bars:
        time.sleep(0.15)
        bars -= 1
        loadtab.setVisible(True)

        if bars != 0:
            loadtab.setValue(11 - bars)
        else:
            loadtab.setVisible(False)