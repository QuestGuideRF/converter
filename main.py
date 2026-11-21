import os
import sys
import tkinter as tk
from tkinter import ttk
from ui .main_window import MainWindow
from utils .theme_manager import ThemeManager
from utils .config_manager import ConfigManager
from utils .file_utils import get_icon_path
def main ():
    root =tk .Tk ()
    root .title ("Конвертер файлов")
    root .geometry ("900x600")
    icon_path =get_icon_path ()
    if icon_path :
        root .iconbitmap (icon_path )
    config =ConfigManager ()
    theme =ThemeManager (root ,config )
    theme .apply_theme ()
    app =MainWindow (root ,config ,theme )
    root .mainloop ()
if __name__ =="__main__":
    directories =[
    "ui","converters","assets/icons","assets/themes",
    "config","utils"
    ]
    for directory in directories :
        os .makedirs (directory ,exist_ok =True )
    main ()