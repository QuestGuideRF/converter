import tkinter as tk
from tkinter import ttk ,messagebox ,filedialog
from ui .image_converter import ImageConverterFrame
from ui .document_converter import DocumentConverterFrame
from ui .video_converter import VideoConverterFrame
from ui .audio_converter import AudioConverterFrame
from ui .archive_converter import ArchiveConverterFrame
from ui .settings_window import SettingsWindow
from utils .file_utils import get_icon_path
class MainWindow :
    def __init__ (self ,root ,config ,theme ):
        self .root =root
        self .config =config
        self .theme =theme
        self .main_frame =ttk .Frame (root )
        self .main_frame .pack (fill =tk .BOTH ,expand =True ,padx =10 ,pady =10 )
        self .current_frame =None
        self ._create_menu ()
        self ._create_main_page ()
    def _create_menu (self ):
        self .menu_bar =tk .Menu (self .root )
        self .root .config (menu =self .menu_bar )
        file_menu =tk .Menu (self .menu_bar ,tearoff =0 )
        file_menu .add_command (label ="Выход",command =self .root .quit )
        settings_menu =tk .Menu (self .menu_bar ,tearoff =0 )
        settings_menu .add_command (label ="Настройки",command =self ._open_settings )
        self .menu_bar .add_cascade (label ="Файл",menu =file_menu )
        self .menu_bar .add_cascade (label ="Настройки",menu =settings_menu )
    def _create_main_page (self ):
        header =ttk .Label (self .main_frame ,text ="Конвертер файлов",font =("Arial",18 ,"bold"))
        header .pack (pady =20 )
        description =ttk .Label (
        self .main_frame ,
        text ="Выберите тип файла для конвертации:",
        font =("Arial",12 )
        )
        description .pack (pady =10 )
        categories_frame =ttk .Frame (self .main_frame )
        categories_frame .pack (fill =tk .BOTH ,expand =True ,padx =20 ,pady =20 )
        for i in range (3 ):
            categories_frame .columnconfigure (i ,weight =1 )
        for i in range (2 ):
            categories_frame .rowconfigure (i ,weight =1 )
        self ._create_category_button (
        categories_frame ,"📄 Документы",0 ,0 ,self ._open_document_converter
        )
        self ._create_category_button (
        categories_frame ,"🖼 Изображения",0 ,1 ,self ._open_image_converter
        )
        self ._create_category_button (
        categories_frame ,"🎥 Видео",0 ,2 ,self ._open_video_converter
        )
        self ._create_category_button (
        categories_frame ,"🔊 Аудио",1 ,0 ,self ._open_audio_converter
        )
        self ._create_category_button (
        categories_frame ,"📦 Архивы",1 ,1 ,self ._open_archive_converter
        )
    def _create_category_button (self ,parent ,text ,row ,col ,command ):
        frame =ttk .Frame (parent ,borderwidth =2 ,relief =tk .GROOVE )
        frame .grid (row =row ,column =col ,padx =10 ,pady =10 ,sticky ="nsew")
        button =ttk .Button (frame ,text =text ,command =command )
        button .pack (fill =tk .BOTH ,expand =True ,padx =20 ,pady =20 )
    def _show_frame (self ,frame_class ):
        for widget in self .main_frame .winfo_children ():
            widget .destroy ()
        self .current_frame =frame_class (self .main_frame ,self .config ,self .theme ,self )
        self .current_frame .pack (fill =tk .BOTH ,expand =True )
        back_button =ttk .Button (
        self .main_frame ,
        text ="← Вернуться на главную",
        command =self ._back_to_main
        )
        back_button .pack (side =tk .BOTTOM ,anchor =tk .W ,padx =10 ,pady =10 )
    def _back_to_main (self ):
        for widget in self .main_frame .winfo_children ():
            widget .destroy ()
        self ._create_main_page ()
    def _open_document_converter (self ):
        self ._show_frame (DocumentConverterFrame )
    def _open_image_converter (self ):
        self ._show_frame (ImageConverterFrame )
    def _open_video_converter (self ):
        self ._show_frame (VideoConverterFrame )
    def _open_audio_converter (self ):
        self ._show_frame (AudioConverterFrame )
    def _open_archive_converter (self ):
        self ._show_frame (ArchiveConverterFrame )
    def _open_settings (self ):
        settings_window =SettingsWindow (self .root ,self .config ,self .theme )
    def update_status (self ,message ):
        pass
    def create_dialog (self ,title ,message ,dialog_type ="info"):
        icon_path =get_icon_path ()
        current_icon =self .root .iconbitmap ()
        if dialog_type =="info":
            result =messagebox .showinfo (title ,message ,parent =self .root )
        elif dialog_type =="warning":
            result =messagebox .showwarning (title ,message ,parent =self .root )
        elif dialog_type =="error":
            result =messagebox .showerror (title ,message ,parent =self .root )
        elif dialog_type =="question":
            result =messagebox .askquestion (title ,message ,parent =self .root )
        else :
            result =messagebox .showinfo (title ,message ,parent =self .root )
        if icon_path and current_icon :
            self .root .iconbitmap (current_icon )
        return result