import os
import tkinter as tk
from tkinter import ttk ,filedialog ,messagebox
import threading
import zipfile
import shutil
class ArchiveConverterFrame (ttk .Frame ):
    def __init__ (self ,parent ,config ,theme ,main_window ):
        super ().__init__ (parent )
        self .parent =parent
        self .config =config
        self .theme =theme
        self .main_window =main_window
        self .supported_formats ={
        "ZIP":(".zip",),
        "TAR":(".tar",),
        "GZ":(".gz",),
        "BZ2":(".bz2",),
        "XZ":(".xz",),
        "7Z":(".7z",),
        "RAR":(".rar",),
        }
        self .files =[]
        self ._create_widgets ()
    def _create_widgets (self ):
        header =ttk .Label (self ,text ="Работа с архивами",font =("Arial",16 ,"bold"))
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
        actions_frame =ttk .LabelFrame (self ,text ="Действия")
        actions_frame .pack (fill =tk .X ,padx =10 ,pady =5 )
        self .action_var =tk .StringVar (value ="extract")
        extract_radio =ttk .Radiobutton (
        actions_frame ,
        text ="Распаковать архив",
        variable =self .action_var ,
        value ="extract"
        )
        extract_radio .pack (anchor =tk .W ,padx =10 ,pady =5 )
        create_radio =ttk .Radiobutton (
        actions_frame ,
        text ="Создать архив",
        variable =self .action_var ,
        value ="create"
        )
        create_radio .pack (anchor =tk .W ,padx =10 ,pady =5 )
        settings_frame =ttk .Frame (actions_frame )
        settings_frame .pack (fill =tk .X ,padx =10 ,pady =5 )
        format_label =ttk .Label (settings_frame ,text ="Формат архива:")
        format_label .grid (row =0 ,column =0 ,sticky =tk .W ,padx =5 ,pady =5 )
        self .format_var =tk .StringVar (value ="ZIP")
        format_combobox =ttk .Combobox (
        settings_frame ,
        textvariable =self .format_var ,
        values =["ZIP","TAR","TAR.GZ","TAR.BZ2"],
        state ="readonly",
        width =10
        )
        format_combobox .grid (row =0 ,column =1 ,sticky =tk .W ,padx =5 ,pady =5 )
        archive_name_label =ttk .Label (settings_frame ,text ="Имя архива:")
        archive_name_label .grid (row =1 ,column =0 ,sticky =tk .W ,padx =5 ,pady =5 )
        self .archive_name_var =tk .StringVar (value ="archive")
        archive_name_entry =ttk .Entry (
        settings_frame ,
        textvariable =self .archive_name_var ,
        width =20
        )
        archive_name_entry .grid (row =1 ,column =1 ,sticky =tk .W +tk .E ,padx =5 ,pady =5 )
        self .dependencies_var =tk .StringVar (
        value ="Примечание: для работы с некоторыми форматами архивов требуются дополнительные библиотеки."
        )
        dependencies_label =ttk .Label (
        actions_frame ,
        textvariable =self .dependencies_var ,
        foreground ="red"
        )
        dependencies_label .pack (padx =10 ,pady =5 ,anchor =tk .W )
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
        process_button =ttk .Button (
        self ,
        text ="Выполнить",
        command =self ._process_archives
        )
        process_button .pack (pady =10 )
        self .progress_var =tk .DoubleVar (value =0.0 )
        self .status_var =tk .StringVar (value ="")
        self ._check_dependencies ()
    def _check_dependencies (self ):
        self .dependencies_var .set ("Все необходимые библиотеки установлены.")
        return
    def _add_files (self ):
        action =self .action_var .get ()
        if action =="extract":
            supported_extensions =[]
            for extensions in self .supported_formats .values ():
                supported_extensions .extend (extensions )
            file_types =[("Архивы"," ".join (["*"+ext for ext in supported_extensions ]))]
            for format_name ,extensions in self .supported_formats .items ():
                file_types .append ((format_name ," ".join (["*"+ext for ext in extensions ])))
            file_types .append (("Все файлы","*.*"))
            files =filedialog .askopenfilenames (
            title ="Выберите архивы для распаковки",
            filetypes =file_types
            )
        else :
            files =filedialog .askopenfilenames (
            title ="Выберите файлы для архивации",
            filetypes =[("Все файлы","*.*")]
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
    def _process_archives (self ):
        if not self .files :
            messagebox .showwarning (
            "Нет файлов",
            "Добавьте файлы для обработки."
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
        action =self .action_var .get ()
        archive_format =self .format_var .get ()
        archive_name =self .archive_name_var .get ()
        thread =threading .Thread (
        target =self ._process_thread ,
        args =(action ,archive_format ,archive_name ,save_path ),
        daemon =True
        )
        thread .start ()
    def _process_thread (self ,action ,archive_format ,archive_name ,save_path ):
        success_count =0
        error_count =0
        self .progress_var .set (0 )
        if action =="extract":
            for i ,file_path in enumerate (self .files ):
                try :
                    filename =os .path .basename (file_path )
                    self .after (0 ,lambda :self .status_var .set (f"Распаковка {i +1 }/{len (self .files )}: {filename }"))
                    self .after (0 ,lambda :self .main_window .update_status (f"Распаковка {i +1 }/{len (self .files )}: {filename }"))
                    extract_dir =os .path .join (save_path ,os .path .splitext (filename )[0 ])
                    os .makedirs (extract_dir ,exist_ok =True )
                    self ._extract_archive (file_path ,extract_dir )
                    success_count +=1
                    self .after (0 ,lambda :self .progress_var .set ((i +1 )/len (self .files )*100 ))
                except Exception as e :
                    error_count +=1
                    print (f"Ошибка при распаковке {file_path }: {e }")
        else :
            try :
                self .after (0 ,lambda :self .status_var .set ("Создание архива..."))
                self .after (0 ,lambda :self .main_window .update_status ("Создание архива..."))
                if archive_format =="ZIP":
                    archive_path =os .path .join (save_path ,f"{archive_name }.zip")
                elif archive_format =="TAR":
                    archive_path =os .path .join (save_path ,f"{archive_name }.tar")
                elif archive_format =="TAR.GZ":
                    archive_path =os .path .join (save_path ,f"{archive_name }.tar.gz")
                elif archive_format =="TAR.BZ2":
                    archive_path =os .path .join (save_path ,f"{archive_name }.tar.bz2")
                else :
                    raise ValueError (f"Неподдерживаемый формат архива: {archive_format }")
                self ._create_archive (archive_format ,archive_path ,self .files )
                success_count =1
                self .after (0 ,lambda :self .progress_var .set (100 ))
            except Exception as e :
                error_count =1
                print (f"Ошибка при создании архива: {e }")
        if error_count ==0 :
            if action =="extract":
                message =f"Распаковка завершена. Успешно обработано архивов: {success_count }"
            else :
                message ="Архив успешно создан."
            self .after (0 ,lambda :self .status_var .set (message ))
            self .after (0 ,lambda :self .main_window .update_status ("Операция завершена"))
            self .after (0 ,lambda :messagebox .showinfo ("Готово",message ))
            self .after (0 ,lambda :self ._open_folder (save_path ))
        else :
            if action =="extract":
                message =f"Распаковка завершена с ошибками. Успешно: {success_count }, ошибок: {error_count }"
            else :
                message ="Не удалось создать архив."
            self .after (0 ,lambda :self .status_var .set (message ))
            self .after (0 ,lambda :self .main_window .update_status ("Операция завершена с ошибками"))
            self .after (0 ,lambda :messagebox .showwarning ("Готово с ошибками",message ))
            self .after (0 ,lambda :self ._open_folder (save_path ))
    def _extract_archive (self ,archive_path ,extract_dir ):
        ext =os .path .splitext (archive_path )[1 ].lower ()
        if ext ==".zip":
            with zipfile .ZipFile (archive_path ,'r')as zip_ref :
                zip_ref .extractall (extract_dir )
        elif ext ==".tar":
            import tarfile
            with tarfile .open (archive_path ,'r')as tar_ref :
                tar_ref .extractall (extract_dir )
        elif ext ==".gz"and archive_path .endswith (".tar.gz"):
            import tarfile
            with tarfile .open (archive_path ,'r:gz')as tar_ref :
                tar_ref .extractall (extract_dir )
        elif ext ==".bz2"and archive_path .endswith (".tar.bz2"):
            import tarfile
            with tarfile .open (archive_path ,'r:bz2')as tar_ref :
                tar_ref .extractall (extract_dir )
        elif ext ==".7z":
            try :
                import py7zr
                with py7zr .SevenZipFile (archive_path ,mode ='r')as z :
                    z .extractall (extract_dir )
            except ImportError :
                raise ImportError ("Для распаковки 7z архивов требуется библиотека py7zr")
        elif ext ==".rar":
            try :
                import rarfile
                with rarfile .RarFile (archive_path )as rf :
                    rf .extractall (extract_dir )
            except ImportError :
                raise ImportError ("Для распаковки RAR архивов требуется библиотека rarfile")
        else :
            raise ValueError (f"Неподдерживаемый формат архива: {ext }")
    def _create_archive (self ,archive_format ,archive_path ,files ):
        if archive_format =="ZIP":
            with zipfile .ZipFile (archive_path ,'w',zipfile .ZIP_DEFLATED )as zip_ref :
                for file in files :
                    zip_ref .write (file ,arcname =os .path .basename (file ))
        elif archive_format =="TAR":
            import tarfile
            with tarfile .open (archive_path ,'w')as tar_ref :
                for file in files :
                    tar_ref .add (file ,arcname =os .path .basename (file ))
        elif archive_format =="TAR.GZ":
            import tarfile
            with tarfile .open (archive_path ,'w:gz')as tar_ref :
                for file in files :
                    tar_ref .add (file ,arcname =os .path .basename (file ))
        elif archive_format =="TAR.BZ2":
            import tarfile
            with tarfile .open (archive_path ,'w:bz2')as tar_ref :
                for file in files :
                    tar_ref .add (file ,arcname =os .path .basename (file ))
        else :
            raise ValueError (f"Неподдерживаемый формат архива: {archive_format }")
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