# -*- coding: utf-8 -*-
import MLabsPy as m

## tkinter example
# https://stackoverflow.com/questions/20790926/ipython-notebook-open-select-file-with-gui-qt-dialog
# answered Sep 24 '19 at 23:50 Alireza Honarfar
#try:
#    from tkinter import Tk
#    from tkFileDialog import askopenfilenames
#except:
#    from tkinter import Tk
#    from tkinter import filedialog

#Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

#file = filedialog.askopenfilenames() # show an "Open" dialog box and return the path to the selected file


ML = m.MLabsPy('MLabsPy3.CSV')
m = ML.getCSVdata('damps')

y = len(m)
x = 0
CSV = []
while x < y:
    l = []
    xx = 0
    yy = len(m)
    while xx < yy:
        l.append(m[x][xx])
        xx += 1
    CSV.append(l)
    x =+ 1

print(CSV)