import os
import tkinter as tk
from tkinter import ttk ,filedialog ,messagebox
import threading
class AudioConverterFrame (ttk .Frame ):
    def __init__ (self ,parent ,config ,theme ,main_window ):
        super ().__init__ (parent )
        self .parent =parent
        self .config =config
        self .theme =theme
        self .main_window =main_window
        self .supported_formats ={
        "MP3":(".mp3",),
        "WAV":(".wav",),
        "OGG":(".ogg",),
        "FLAC":(".flac",),
        "AAC":(".aac",),
        "M4A":(".m4a",),
        "WMA":(".wma",),
        }
        self .files =[]
        self ._create_widgets ()
    def _create_widgets (self ):
        header =ttk .Label (self ,text ="Конвертер аудио",font =("Arial",16 ,"bold"))
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
        self .format_var =tk .StringVar (value ="MP3")
        format_combobox =ttk .Combobox (
        format_frame ,
        textvariable =self .format_var ,
        values =list (self .supported_formats .keys ()),
        state ="readonly",
        width =10
        )
        format_combobox .pack (side =tk .LEFT ,padx =5 )
        bitrate_frame =ttk .Frame (settings_frame )
        bitrate_frame .pack (fill =tk .X ,padx =5 ,pady =5 )
        bitrate_label =ttk .Label (bitrate_frame ,text ="Битрейт:")
        bitrate_label .pack (side =tk .LEFT ,padx =5 )
        self .bitrate_var =tk .StringVar (value ="192k")
        bitrate_combobox =ttk .Combobox (
        bitrate_frame ,
        textvariable =self .bitrate_var ,
        values =["128k","192k","256k","320k"],
        state ="readonly",
        width =10
        )
        bitrate_combobox .pack (side =tk .LEFT ,padx =5 )
        channels_frame =ttk .Frame (settings_frame )
        channels_frame .pack (fill =tk .X ,padx =5 ,pady =5 )
        channels_label =ttk .Label (channels_frame ,text ="Каналы:")
        channels_label .pack (side =tk .LEFT ,padx =5 )
        self .channels_var =tk .StringVar (value ="Оригинальные")
        channels_combobox =ttk .Combobox (
        channels_frame ,
        textvariable =self .channels_var ,
        values =["Оригинальные","Моно","Стерео"],
        state ="readonly",
        width =15
        )
        channels_combobox .pack (side =tk .LEFT ,padx =5 )
        self .dependencies_var =tk .StringVar (
        value ="Примечание: для конвертации аудио требуется библиотека pydub."
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
        command =self ._convert_audio
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
        file_types =[("Аудио"," ".join (["*"+ext for ext in supported_extensions ]))]
        for format_name ,extensions in self .supported_formats .items ():
            file_types .append ((format_name ," ".join (["*"+ext for ext in extensions ])))
        file_types .append (("Все файлы","*.*"))
        files =filedialog .askopenfilenames (
        title ="Выберите аудио",
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
    def _convert_audio (self ):
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
        bitrate =self .bitrate_var .get ()
        channels =self .channels_var .get ()
        thread =threading .Thread (
        target =self ._convert_thread ,
        args =(target_extension ,bitrate ,channels ,save_path ),
        daemon =True
        )
        thread .start ()
    def _convert_thread (self ,target_extension ,bitrate ,channels ,save_path ):
        try :
            from pydub import AudioSegment
        except ImportError :
            self .after (0 ,lambda :messagebox .showerror (
            "Ошибка",
            "Для конвертации аудио требуется библиотека pydub. Установите её командой:\n"
            "pip установить pydub"
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
                source_extension =os .path .splitext (file_path )[1 ].lower ()
                source_format =source_extension [1 :]
                base_name =os .path .splitext (os .path .basename (file_path ))[0 ]
                output_file =os .path .join (save_path ,f"{base_name }{target_extension }")
                counter =1
                while os .path .exists (output_file ):
                    output_file =os .path .join (save_path ,f"{base_name }_{counter }{target_extension }")
                    counter +=1
                audio =AudioSegment .from_file (file_path ,format =source_format )
                if channels =="Моно"and audio .channels >1 :
                    audio =audio .set_channels (1 )
                elif channels =="Стерео"and audio .channels ==1 :
                    audio =audio .set_channels (2 )
                bitrate_value =int (bitrate .replace ("k",""))*1000
                target_format =target_extension [1 :]
                audio .export (
                output_file ,
                format =target_format ,
                bitrate =bitrate
                )
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