#!/usr/bin/env python3
import os

import gui

if __name__ == '__main__':
    gui = gui.GUI()

    if os.path.exists('./images/parameter.txt'):
        gui.load_image_path('./images')

    gui.mainloop()
