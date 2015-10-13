import Tkinter as tk
#!/usr/bin/python

import pexpect
import time
from time import gmtime, strftime, sleep


mode = "NULL"
busSpeed = "NULL"
date = strftime("%m/%d/%Y %H:%M:%S")




child = pexpect.spawn('ssh root@17.246.22.100')
counter = 0
def counter_label(label):
    def count():
        global counter
        
        child.expect('#', timeout=None)
        child.sendline("accctl list | grep 'USB connect state'; ioreg -lxw0 -r -c IOUSBHostDevice | grep -i USBSpeed | tail -n 1")
        
        i = child.expect(['host', 'device', 'none'], timeout=None)
        j = child.expect(['0x0', '0x1', '0x2', '0x3', '0x4'], timeout=None)
        
        if i == 0:
            mode = "DEVICE MODE"
        elif i == 1:
            mode = "HOST MODE"
        else:
            mode = "NOT CONNECTED"
        
        if j == 0:
            busSpeed = "NO CONNECTION"
        elif j == 1:
            busSpeed = "FULL SPEED"
        elif j == 2:
            busSpeed = "LOW SPEED"
        elif j == 3:
            busSpeed = "HIGH SPEED"
        elif j == 4:
            busSpeed = "SUPER SPEED"
        else:
            busSpeed = "NOT CONNECTED"
        
        date = strftime("%m/%d/%Y %H:%M:%S")
        
        counter = 'Mode: ' + mode + '     Bus Speed: ' + busSpeed #+ '     Date: ' + date
        print 'Mode: ' + mode + '     Bus Speed: ' + busSpeed + '     Date: ' + date
        
        
        label.config(text=str(counter))
        label.after(200, count)
    count()


root = tk.Tk()
root.title("Device Status")
label = tk.Label(root, fg="black")
label.pack()
counter_label(label)
button = tk.Button(root, text='Stop', width=25, command=root.destroy)
button.pack()
root.mainloop()
