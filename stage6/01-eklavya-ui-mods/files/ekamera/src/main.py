#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Main

from EKamera import EKamera
from Exceptions_ModuleCamera import TkinterError, EKameraError
from tkinter import Tk, messagebox, PhotoImage
from picamera import PiCamera

# Exécute le programme
def run():
    try:
        camera = PiCamera()  # Mode autre que 0 pour pouvoir changer de mode plus tard
        camera.sensor_mode = 0	# Retourne au mode 0
    except:
        messagebox.showerror("EKamera error", "Camera initialization error\nIt may be badly installed\nIf it still doesn't work,\nplease restart the system")
        raise EKameraError("Error creating the EKamera instance")
        print("Finished")
        return 0
    photo = PhotoImage(file = "/etc/eklavya/ekamera/ekamera.png")
    win.iconphoto(False, photo)
    win.resizable(width=False, height=False)
    app = EKamera(win,camera,title="EKamera")
    win.protocol("WM_DELETE_WINDOW", callback)
    win.mainloop()

    camera.close()

def callback():
    if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        win.destroy()

# Exécute le programme
if __name__ == "__main__":
    print("Window initialization")
    try:
        win = Tk()
    except:
        messagebox.showerror("Tkinter error", "GUI initialization error")
        raise TkinterError("Tkinter initialization error")
        print("Finished")
    run()
