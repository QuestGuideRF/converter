import tkinter as tk
from tkinter import ttk
class ThemeManager :
    def __init__ (self ,root ,config ):
        self .root =root
        self .config =config
        self .themes ={
        "light":{
        "bg":"#f0f0f0",
        "fg":"#000000",
        "accent":"#4a7abc",
        "button_bg":"#e0e0e0",
        "button_fg":"#000000",
        "entry_bg":"#ffffff",
        "entry_fg":"#000000",
        "highlight_bg":"#d0d0d0",
        "highlight_fg":"#000000"
        },
        "dark":{
        "bg":"#1а1а1а",
        "fg":"#ffffff",
        "accent":"#5c8dd6",
        "button_bg":"#2c2c2c",
        "button_fg":"#ffffff",
        "entry_bg":"#2c2c2c",
        "entry_fg":"#ffffff",
        "highlight_bg":"#3c3c3c",
        "highlight_fg":"#ffffff"
        }
        }
        self .current_theme =self .config .get ("theme","light")
    def apply_theme (self ):
        theme =self .themes [self .current_theme ]
        style =ttk .Style ()
        style .theme_use ("clam")
        style .configure ("TFrame",background =theme ["bg"])
        style .configure ("TLabel",background =theme ["bg"],foreground =theme ["fg"])
        style .configure ("TLabelFrame",
        background =theme ["bg"],
        foreground =theme ["fg"])
        style .configure ("TLabelFrame.Label",
        background =theme ["bg"],
        foreground =theme ["fg"])
        style .configure ("TButton",
        background =theme ["button_bg"],
        foreground =theme ["button_fg"],
        borderwidth =1 ,
        focuscolor =theme ["accent"])
        style .map ("TButton",
        background =[("active",theme ["highlight_bg"])],
        foreground =[("active",theme ["highlight_fg"])])
        style .configure ("TEntry",
        fieldbackground =theme ["entry_bg"],
        foreground =theme ["entry_fg"],
        bordercolor =theme ["accent"])
        style .configure ("TCombobox",
        fieldbackground =theme ["entry_bg"],
        foreground =theme ["entry_fg"],
        bordercolor =theme ["accent"])
        style .map ("TCombobox",
        fieldbackground =[("readonly",theme ["entry_bg"])],
        selectbackground =[("readonly",theme ["accent"])])
        style .configure ("TCheckbutton",
        background =theme ["bg"],
        foreground =theme ["fg"])
        style .configure ("TRadiobutton",
        background =theme ["bg"],
        foreground =theme ["fg"])
        style .configure ("TProgressbar",
        background =theme ["accent"],
        troughcolor =theme ["bg"])
        style .configure ("TNotebook",
        background =theme ["bg"],
        foreground =theme ["fg"])
        style .configure ("TNotebook.Tab",
        background =theme ["button_bg"],
        foreground =theme ["button_fg"],
        padding =[10 ,5 ])
        style .map ("TNotebook.Tab",
        background =[("selected",theme ["accent"])],
        foreground =[("selected",theme ["highlight_fg"])])
        self .root .configure (background =theme ["bg"])
        self .root .option_add ("*Listbox.background",theme ["entry_bg"])
        self .root .option_add ("*Listbox.foreground",theme ["entry_fg"])
        self .root .option_add ("*Текст.фон",theme ["entry_bg"])
        self .root .option_add ("*Текст.передний план",theme ["entry_fg"])
        self .root .option_add ("*Вступление.фон",theme ["entry_bg"])
        self .root .option_add ("*Entry.передний план",theme ["entry_fg"])
        self .root .option_add ("*Меню.фон",theme ["bg"])
        self .root .option_add ("*Меню.передний план",theme ["fg"])
        self .root .option_add ("*Menu.activeBackground",theme ["highlight_bg"])
        self .root .option_add ("*Menu.activeForeground",theme ["highlight_fg"])
    def set_theme (self ,theme_name ):
        if theme_name in self .themes :
            self .current_theme =theme_name
            self .config .set ("theme",theme_name )
            self .apply_theme ()
    def toggle_theme (self ):
        if self .current_theme =="light":
            self .set_theme ("dark")
        else :
            self .set_theme ("light")
    def get_current_theme (self ):
        return self .current_theme