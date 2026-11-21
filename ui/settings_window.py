import os
import tkinter as tk
from tkinter import ttk ,filedialog
from utils .file_utils import get_icon_path
class SettingsWindow :
    def __init__ (self ,parent ,config ,theme ):
        self .parent =parent
        self .config =config
        self .theme =theme
        self .window =tk .Toplevel (parent )
        self .window .title ("Настройки")
        self .window .geometry ("500x400")
        self .window .resizable (False ,False )
        self .window .transient (parent )
        self .window .grab_set ()
        icon_path =get_icon_path ()
        if icon_path :
            self .window .iconbitmap (icon_path )
        self .window .update_idletasks ()
        width =self .window .winfo_width ()
        height =self .window .winfo_height ()
        x =(self .window .winfo_screenwidth ()//2 )-(width //2 )
        y =(self .window .winfo_screenheight ()//2 )-(height //2 )
        self .window .geometry (f'{width }x{height }+{x }+{y }')
        self .window .configure (background =self .theme .themes [self .theme .current_theme ]["bg"])
        self ._create_notebook ()
        self ._create_buttons ()
    def _create_notebook (self ):
        self .notebook =ttk .Notebook (self .window )
        self .notebook .pack (fill =tk .BOTH ,expand =True ,padx =10 ,pady =10 )
        self .appearance_tab =ttk .Frame (self .notebook )
        self .paths_tab =ttk .Frame (self .notebook )
        self .notebook .add (self .appearance_tab ,text ="Внешний вид")
        self .notebook .add (self .paths_tab ,text ="Пути")
        self ._create_appearance_tab ()
        self ._create_paths_tab ()
    def _create_appearance_tab (self ):
        appearance_frame =ttk .Frame (self .appearance_tab ,padding =10 )
        appearance_frame .pack (fill =tk .BOTH ,expand =True )
        theme_frame =ttk .Frame (appearance_frame )
        theme_frame .pack (fill =tk .X ,pady =5 )
        theme_label =ttk .Label (theme_frame ,text ="Тема оформления:")
        theme_label .pack (side =tk .LEFT )
        self .theme_var =tk .StringVar (value =self .theme .current_theme )
        light_radio =ttk .Radiobutton (
        theme_frame ,
        text ="Светлая",
        variable =self .theme_var ,
        value ="light",
        command =lambda :self .theme .set_theme ("light")
        )
        light_radio .pack (side =tk .RIGHT )
        dark_radio =ttk .Radiobutton (
        theme_frame ,
        text ="Темная",
        variable =self .theme_var ,
        value ="dark",
        command =lambda :self .theme .set_theme ("dark")
        )
        dark_radio .pack (side =tk .RIGHT ,padx =10 )
        ttk .Separator (appearance_frame ,orient =tk .HORIZONTAL ).pack (fill =tk .X ,pady =10 )
        size_frame =ttk .Frame (appearance_frame )
        size_frame .pack (fill =tk .X ,pady =5 )
        size_label =ttk .Label (size_frame ,text ="Размер окна:")
        size_label .pack (side =tk .LEFT )
        self .size_var =tk .StringVar (value =self .config .get ("window_size","default"))
        default_radio =ttk .Radiobutton (
        size_frame ,
        text ="По умолчанию",
        variable =self .size_var ,
        value ="default"
        )
        default_radio .pack (anchor =tk .W )
        fullscreen_radio =ttk .Radiobutton (
        size_frame ,
        text ="На весь экран",
        variable =self .size_var ,
        value ="fullscreen"
        )
        fullscreen_radio .pack (anchor =tk .W )
        custom_radio =ttk .Radiobutton (
        size_frame ,
        text ="Пользовательский",
        variable =self .size_var ,
        value ="custom"
        )
        custom_radio .pack (anchor =tk .W )
        custom_frame =ttk .Frame (appearance_frame )
        custom_frame .pack (fill =tk .X ,pady =5 )
        width_label =ttk .Label (custom_frame ,text ="Ширина:")
        width_label .grid (row =0 ,column =0 ,padx =5 )
        self .width_var =tk .StringVar (value =str (self .config .get ("custom_width",900 )))
        width_entry =ttk .Entry (custom_frame ,textvariable =self .width_var ,width =5 )
        width_entry .grid (row =0 ,column =1 ,padx =5 )
        height_label =ttk .Label (custom_frame ,text ="Высота:")
        height_label .grid (row =0 ,column =2 ,padx =5 )
        self .height_var =tk .StringVar (value =str (self .config .get ("custom_height",600 )))
        height_entry =ttk .Entry (custom_frame ,textvariable =self .height_var ,width =5 )
        height_entry .grid (row =0 ,column =3 ,padx =5 )
        ttk .Separator (appearance_frame ,orient =tk .HORIZONTAL ).pack (fill =tk .X ,pady =10 )
        default_button =ttk .Button (
        appearance_frame ,
        text ="Сбросить настройки к значениям по умолчанию",
        command =self ._reset_settings
        )
        default_button .pack (pady =10 )
    def _create_paths_tab (self ):
        paths_frame =ttk .Frame (self .paths_tab ,padding =10 )
        paths_frame .pack (fill =tk .BOTH ,expand =True )
        save_path_frame =ttk .Frame (paths_frame )
        save_path_frame .pack (fill =tk .X ,pady =5 )
        save_path_label =ttk .Label (save_path_frame ,text ="Путь сохранения по умолчанию:")
        save_path_label .pack (anchor =tk .W )
        save_path_input_frame =ttk .Frame (save_path_frame )
        save_path_input_frame .pack (fill =tk .X ,pady =5 )
        self .save_path_var =tk .StringVar (value =self .config .get ("default_save_path",os .path .expanduser ("~/Загрузки")))
        save_path_entry =ttk .Entry (save_path_input_frame ,textvariable =self .save_path_var )
        save_path_entry .pack (side =tk .LEFT ,fill =tk .X ,expand =True )
        save_path_button =ttk .Button (
        save_path_input_frame ,
        text ="Обзор...",
        command =self ._browse_save_path
        )
        save_path_button .pack (side =tk .RIGHT ,padx =5 )
        ttk .Separator (paths_frame ,orient =tk .HORIZONTAL ).pack (fill =tk .X ,pady =10 )
        recent_label =ttk .Label (paths_frame ,text ="Недавно использованные папки:")
        recent_label .pack (anchor =tk .W ,pady =5 )
        recent_folders =self .config .get ("recent_folders",[])
        if recent_folders :
            for folder in recent_folders :
                folder_frame =ttk .Frame (paths_frame )
                folder_frame .pack (fill =tk .X ,pady =2 )
                folder_label =ttk .Label (folder_frame ,text =folder ,anchor =tk .W )
                folder_label .pack (side =tk .LEFT ,fill =tk .X ,expand =True )
                folder_button =ttk .Button (
                folder_frame ,
                text ="Использовать",
                command =lambda f =folder :self ._use_folder (f )
                )
                folder_button .pack (side =tk .RIGHT )
        else :
            no_folders_label =ttk .Label (paths_frame ,text ="Нет недавно использованных папок")
            no_folders_label .pack (anchor =tk .W ,pady =5 )
    def _create_buttons (self ):
        buttons_frame =ttk .Frame (self .window )
        buttons_frame .pack (fill =tk .X ,pady =10 ,padx =10 )
        save_button =ttk .Button (
        buttons_frame ,
        text ="Сохранить",
        command =self ._save_settings
        )
        save_button .pack (side =tk .RIGHT ,padx =5 )
        cancel_button =ttk .Button (
        buttons_frame ,
        text ="Отмена",
        command =self .window .destroy
        )
        cancel_button .pack (side =tk .RIGHT ,padx =5 )
    def _save_settings (self ):
        self .config .set ("theme",self .theme_var .get ())
        self .config .set ("window_size",self .size_var .get ())
        try :
            custom_width =int (self .width_var .get ())
            custom_height =int (self .height_var .get ())
            if custom_width <640 :
                custom_width =640
            if custom_height <480 :
                custom_height =480
            self .config .set ("custom_width",custom_width )
            self .config .set ("custom_height",custom_height )
        except ValueError :
            self .config .set ("custom_width",900 )
            self .config .set ("custom_height",600 )
        self .config .set ("default_save_path",self .save_path_var .get ())
        window_size =self .size_var .get ()
        if window_size =="default":
            self .parent .geometry ("900x600")
        elif window_size =="fullscreen":
            self .parent .attributes ("-fullscreen",True )
        elif window_size =="custom":
            custom_width =self .config .get ("custom_width",900 )
            custom_height =self .config .get ("custom_height",600 )
            self .parent .geometry (f"{custom_width }x{custom_height }")
        self .window .destroy ()
    def _reset_settings (self ):
        self .config .reset ()
        self .theme_var .set (self .config .get ("theme","light"))
        self .size_var .set (self .config .get ("window_size","default"))
        self .width_var .set (str (self .config .get ("custom_width",900 )))
        self .height_var .set (str (self .config .get ("custom_height",600 )))
        self .save_path_var .set (self .config .get ("default_save_path",os .path .expanduser ("~/Загрузки")))
        self .theme .set_theme (self .config .get ("theme","light"))
    def _browse_save_path (self ):
        folder =filedialog .askdirectory (
        initialdir =self .save_path_var .get (),
        title ="Выберите папку для сохранения"
        )
        if folder :
            self .save_path_var .set (folder )
    def _use_folder (self ,folder ):
        self .save_path_var .set (folder )