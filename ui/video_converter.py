import os
import tkinter as tk
from tkinter import ttk ,filedialog ,messagebox
import threading
class VideoConverterFrame (ttk .Frame ):
    def __init__ (self ,parent ,config ,theme ,main_window ):
        super ().__init__ (parent )
        self .parent =parent
        self .config =config
        self .theme =theme
        self .main_window =main_window
        self .supported_formats ={
        "MP4":(".mp4",),
        "AVI":(".avi",),
        "MKV":(".mkv",),
        "MOV":(".mov",),
        "WMV":(".wmv",),
        "FLV":(".flv",),
        "WEBM":(".webm",),
        }
        self .files =[]
        self ._create_widgets ()
    def _create_widgets (self ):
        header =ttk .Label (self ,text ="Конвертер видео",font =("Arial",16 ,"bold"))
        header .pack (pady =10 )
        files_frame =ttk .LabelFrame (self ,text ="Выбор файлов")
        files_frame .pack (fill =tk .X ,padx =10 ,pady =5 )
        buttons_frame =ttk .Frame (files_frame )
        buttons_frame .pack (fill =tk .X ,padx =5 ,pady =5 )
        add_button =ttk .Button (
        buttons_frame ,
        text ="Добавить файлы",
        command =self ._add_files
        )
        add_button .pack (side =tk .LEFT ,padx =5 )
        clear_button =ttk .Button (
        buttons_frame ,
        text ="Очистить список",
        command =self ._clear_files
        )
        clear_button .pack (side =tk .LEFT ,padx =5 )
        self .files_listbox =tk .Listbox (
        files_frame ,
        selectmode =tk .EXTENDED ,
        height =5
        )
        self .files_listbox .pack (fill =tk .X ,padx =5 ,pady =5 )
        self .files_listbox .bind ("<Удалить>",self ._remove_selected_files )
        settings_frame =ttk .LabelFrame (self ,text ="Настройки конвертации")
        settings_frame .pack (fill =tk .X ,padx =10 ,pady =5 )
        format_frame =ttk .Frame (settings_frame )
        format_frame .pack (fill =tk .X ,padx =5 ,pady =5 )
        format_label =ttk .Label (format_frame ,text ="Формат:")
        format_label .pack (side =tk .LEFT ,padx =5 )
        self .format_var =tk .StringVar (value ="MP4")
        format_combobox =ttk .Combobox (
        format_frame ,
        textvariable =self .format_var ,
        values =list (self .supported_formats .keys ()),
        state ="readonly",
        width =10
        )
        format_combobox .pack (side =tk .LEFT ,padx =5 )
        resolution_frame =ttk .Frame (settings_frame )
        resolution_frame .pack (fill =tk .X ,padx =5 ,pady =5 )
        resolution_label =ttk .Label (resolution_frame ,text ="Разрешение:")
        resolution_label .pack (side =tk .LEFT ,padx =5 )
        self .resolution_var =tk .StringVar (value ="Оригинальное")
        resolution_combobox =ttk .Combobox (
        resolution_frame ,
        textvariable =self .resolution_var ,
        values =["Оригинальное","1080p","720p","480p","360p"],
        state ="readonly",
        width =15
        )
        resolution_combobox .pack (side =tk .LEFT ,padx =5 )
        bitrate_frame =ttk .Frame (settings_frame )
        bitrate_frame .pack (fill =tk .X ,padx =5 ,pady =5 )
        bitrate_label =ttk .Label (bitrate_frame ,text ="Битрейт:")
        bitrate_label .pack (side =tk .LEFT ,padx =5 )
        self .bitrate_var =tk .StringVar (value ="Оригинальный")
        bitrate_combobox =ttk .Combobox (
        bitrate_frame ,
        textvariable =self .bitrate_var ,
        values =["Оригинальный","1000k","2000k","3000k","5000k","8000k"],
        state ="readonly",
        width =15
        )
        bitrate_combobox .pack (side =tk .LEFT ,padx =5 )
        self .dependencies_var =tk .StringVar (
        value ="Примечание: для конвертации видео требуется библиотека moviepy."
        )
        dependencies_label =ttk .Label (
        settings_frame ,
        textvariable =self .dependencies_var ,
        foreground ="red"
        )
        dependencies_label .pack (padx =5 ,pady =5 ,anchor =tk .W )
        save_frame =ttk .LabelFrame (self ,text ="Сохранение")
        save_frame .pack (fill =tk .X ,padx =10 ,pady =5 )
        path_frame =ttk .Frame (save_frame )
        path_frame .pack (fill =tk .X ,padx =5 ,pady =5 )
        path_label =ttk .Label (path_frame ,text ="Путь сохранения:")
        path_label .pack (side =tk .LEFT ,padx =5 )
        self .save_path_var =tk .StringVar (value =self .config .get ("default_save_path",os .path .expanduser ("~/Загрузки")))
        path_entry =ttk .Entry (path_frame ,textvariable =self .save_path_var )
        path_entry .pack (side =tk .LEFT ,fill =tk .X ,expand =True ,padx =5 )
        browse_button =ttk .Button (
        path_frame ,
        text ="Обзор...",
        command =self ._browse_save_path
        )
        browse_button .pack (side =tk .RIGHT ,padx =5 )
        convert_button =ttk .Button (
        self ,
        text ="Конвертировать",
        command =self ._convert_videos
        )
        convert_button .pack (pady =10 )
        self .progress_var =tk .DoubleVar (value =0.0 )
        self .status_var =tk .StringVar (value ="")
        self ._check_dependencies ()
    def _check_dependencies (self ):
        self .dependencies_var .set ("Все необходимые библиотеки установлены.")
        return
    def _add_files (self ):
        supported_extensions =[]
        for extensions in self .supported_formats .values ():
            supported_extensions .extend (extensions )
        file_types =[("Видео"," ".join (["*"+ext for ext in supported_extensions ]))]
        for format_name ,extensions in self .supported_formats .items ():
            file_types .append ((format_name ," ".join (["*"+ext for ext in extensions ])))
        file_types .append (("Все файлы","*.*"))
        files =filedialog .askopenfilenames (
        title ="Выберите видео",
        filetypes =file_types
        )
        if files :
            if len (self .files )+len (files )>10 :
                messagebox .showwarning (
                "Превышен лимит",
                "Можно выбрать не более 10 файлов одновременно."
                )
                return
            for file in files :
                if file not in self .files :
                    self .files .append (file )
                    self .files_listbox .insert (tk .END ,os .path .basename (file ))
            self .status_var .set (f"Выбрано файлов: {len (self .files )}")
            self .main_window .update_status (f"Выбрано файлов: {len (self .files )}")
    def _clear_files (self ):
        self .files =[]
        self .files_listbox .delete (0 ,tk .END )
        self .status_var .set ("Список файлов очищен")
        self .main_window .update_status ("Список файлов очищен")
    def _remove_selected_files (self ,event =None ):
        selected_indices =self .files_listbox .curselection ()
        if not selected_indices :
            return
        for i in sorted (selected_indices ,reverse =True ):
            del self .files [i ]
            self .files_listbox .delete (i )
        self .status_var .set (f"Выбрано файлов: {len (self .files )}")
        self .main_window .update_status (f"Выбрано файлов: {len (self .files )}")
    def _browse_save_path (self ):
        folder =filedialog .askdirectory (
        initialdir =self .save_path_var .get (),
        title ="Выберите папку для сохранения"
        )
        if folder :
            self .save_path_var .set (folder )
            self .config .add_recent_folder (folder )
    def _convert_videos (self ):
        if not self .files :
            messagebox .showwarning (
            "Нет файлов",
            "Добавьте файлы для конвертации."
            )
            return
        save_path =self .save_path_var .get ()
        if not os .path .exists (save_path ):
            try :
                os .makedirs (save_path ,exist_ok =True )
            except Exception as e :
                messagebox .showerror (
                "Ошибка",
                f"Не удалось создать папку для сохранения: {e }"
                )
                return
        target_format =self .format_var .get ()
        target_extension =self .supported_formats [target_format ][0 ]
        resolution =self .resolution_var .get ()
        bitrate =self .bitrate_var .get ()
        thread =threading .Thread (
        target =self ._convert_thread ,
        args =(target_extension ,resolution ,bitrate ,save_path ),
        daemon =True
        )
        thread .start ()
    def _convert_thread (self ,target_extension ,resolution ,bitrate ,save_path ):
        try :
            import moviepy .editor as mp
        except ImportError :
            self .after (0 ,lambda :messagebox .showerror (
            "Ошибка",
            "Для конвертации видео требуется библиотека moviepy. Установите её командой:\n"
            "pip установить Moviepy"
            ))
            return
        success_count =0
        error_count =0
        self .progress_var .set (0 )
        for i ,file_path in enumerate (self .files ):
            try :
                filename =os .path .basename (file_path )
                self .after (0 ,lambda :self .status_var .set (f"Конвертация {i +1 }/{len (self .files )}: {filename }"))
                self .after (0 ,lambda :self .main_window .update_status (f"Конвертация {i +1 }/{len (self .files )}: {filename }"))
                base_name =os .path .splitext (os .path .basename (file_path ))[0 ]
                output_file =os .path .join (save_path ,f"{base_name }{target_extension }")
                counter =1
                while os .path .exists (output_file ):
                    output_file =os .path .join (save_path ,f"{base_name }_{counter }{target_extension }")
                    counter +=1
                video =mp .VideoFileClip (file_path )
                if resolution !="Оригинальное":
                    height =int (resolution .replace ("p",""))
                    width =int (video .w *height /video .h )
                    video =video .resize (height =height )
                if bitrate !="Оригинальный":
                    video .write_videofile (output_file ,bitrate =bitrate )
                else :
                    video .write_videofile (output_file )
                video .close ()
                success_count +=1
                self .after (0 ,lambda :self .progress_var .set ((i +1 )/len (self .files )*100 ))
            except Exception as e :
                error_count +=1
                print (f"Ошибка при конвертации {file_path }: {e }")
        if error_count ==0 :
            message =f"Конвертация завершена. Успешно обработано файлов: {success_count }"
            self .after (0 ,lambda :self .status_var .set (message ))
            self .after (0 ,lambda :self .main_window .update_status ("Конвертация завершена"))
            self .after (0 ,lambda :messagebox .showinfo ("Готово",message ))
            self .after (0 ,lambda :self ._open_folder (save_path ))
        else :
            message =f"Конвертация завершена с ошибками. Успешно: {success_count }, ошибок: {error_count }"
            self .after (0 ,lambda :self .status_var .set (message ))
            self .after (0 ,lambda :self .main_window .update_status ("Конвертация завершена с ошибками"))
            self .after (0 ,lambda :messagebox .showwarning ("Готово с ошибками",message ))
            self .after (0 ,lambda :self ._open_folder (save_path ))
    def _open_folder (self ,path ):
        if os .path .exists (path ):
            if os .name =='nt':
                os .startfile (path )
            elif os .name =='posix':
                try :
                    import subprocess
                    subprocess .Popen (['xdg-open',path ])
                except :
                    pass