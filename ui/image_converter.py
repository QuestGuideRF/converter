import os
import tkinter as tk
from tkinter import ttk ,filedialog ,messagebox
from PIL import Image ,ImageTk
class ImageConverterFrame (ttk .Frame ):
    def __init__ (self ,parent ,config ,theme ,main_window ):
        super ().__init__ (parent )
        self .parent =parent
        self .config =config
        self .theme =theme
        self .main_window =main_window
        self .supported_formats ={
        "JPEG":(".jpg",".jpeg"),
        "PNG":(".png",),
        "BMP":(".bmp",),
        "GIF":(".gif",),
        "TIFF":(".tif",".tiff"),
        "ICO":(".ico",),
        "WEBP":(".webp",),
        }
        self .files =[]
        self ._create_widgets ()
    def _create_widgets (self ):
        header =ttk .Label (self ,text ="Конвертер изображений",font =("Arial",16 ,"bold"))
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
        self .format_var =tk .StringVar (value ="JPEG")
        format_combobox =ttk .Combobox (
        format_frame ,
        textvariable =self .format_var ,
        values =list (self .supported_formats .keys ()),
        state ="readonly",
        width =10
        )
        format_combobox .pack (side =tk .LEFT ,padx =5 )
        quality_frame =ttk .Frame (settings_frame )
        quality_frame .pack (fill =tk .X ,padx =5 ,pady =5 )
        quality_label =ttk .Label (quality_frame ,text ="Качество:")
        quality_label .pack (side =tk .LEFT ,padx =5 )
        self .quality_var =tk .IntVar (value =85 )
        quality_scale =ttk .Scale (
        quality_frame ,
        from_ =1 ,
        to =100 ,
        orient =tk .HORIZONTAL ,
        variable =self .quality_var ,
        length =200
        )
        quality_scale .pack (side =tk .LEFT ,padx =5 )
        quality_value =ttk .Label (quality_frame ,textvariable =self .quality_var )
        quality_value .pack (side =tk .LEFT ,padx =5 )
        resize_frame =ttk .Frame (settings_frame )
        resize_frame .pack (fill =tk .X ,padx =5 ,pady =5 )
        self .resize_var =tk .BooleanVar (value =False )
        resize_check =ttk .Checkbutton (
        resize_frame ,
        text ="Изменить размер",
        variable =self .resize_var ,
        command =self ._toggle_resize
        )
        resize_check .pack (side =tk .LEFT ,padx =5 )
        width_label =ttk .Label (resize_frame ,text ="Ширина:")
        width_label .pack (side =tk .LEFT ,padx =5 )
        self .width_var =tk .StringVar (value ="")
        width_entry =ttk .Entry (
        resize_frame ,
        textvariable =self .width_var ,
        width =5 ,
        state =tk .DISABLED
        )
        width_entry .pack (side =tk .LEFT ,padx =5 )
        self .width_entry =width_entry
        height_label =ttk .Label (resize_frame ,text ="Высота:")
        height_label .pack (side =tk .LEFT ,padx =5 )
        self .height_var =tk .StringVar (value ="")
        height_entry =ttk .Entry (
        resize_frame ,
        textvariable =self .height_var ,
        width =5 ,
        state =tk .DISABLED
        )
        height_entry .pack (side =tk .LEFT ,padx =5 )
        self .height_entry =height_entry
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
        command =self ._convert_images
        )
        convert_button .pack (pady =10 )
        self .progress_var =tk .DoubleVar (value =0.0 )
        self .status_var =tk .StringVar (value ="")
    def _toggle_resize (self ):
        if self .resize_var .get ():
            self .width_entry .config (state =tk .NORMAL )
            self .height_entry .config (state =tk .NORMAL )
        else :
            self .width_entry .config (state =tk .DISABLED )
            self .height_entry .config (state =tk .DISABLED )
    def _add_files (self ):
        supported_extensions =[]
        for extensions in self .supported_formats .values ():
            supported_extensions .extend (extensions )
        file_types =[("Изображения"," ".join (["*"+ext for ext in supported_extensions ]))]
        for format_name ,extensions in self .supported_formats .items ():
            file_types .append ((format_name ," ".join (["*"+ext for ext in extensions ])))
        file_types .append (("Все файлы","*.*"))
        files =filedialog .askopenfilenames (
        title ="Выберите изображения",
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
    def _clear_files (self ):
        self .files =[]
        self .files_listbox .delete (0 ,tk .END )
        self .status_var .set ("Список файлов очищен")
    def _remove_selected_files (self ,event =None ):
        selected_indices =self .files_listbox .curselection ()
        if not selected_indices :
            return
        for i in sorted (selected_indices ,reverse =True ):
            del self .files [i ]
            self .files_listbox .delete (i )
        self .status_var .set (f"Выбрано файлов: {len (self .files )}")
    def _browse_save_path (self ):
        folder =filedialog .askdirectory (
        initialdir =self .save_path_var .get (),
        title ="Выберите папку для сохранения"
        )
        if folder :
            self .save_path_var .set (folder )
            self .config .add_recent_folder (folder )
    def _convert_images (self ):
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
        output_format =self .format_var .get ()
        quality =self .quality_var .get ()
        width =None
        height =None
        if self .resize_var .get ():
            try :
                width_str =self .width_var .get ().strip ()
                height_str =self .height_var .get ().strip ()
                if width_str :
                    width =int (width_str )
                    if width <=0 :
                        raise ValueError ("Ширина должна быть положительным числом")
                if height_str :
                    height =int (height_str )
                    if height <=0 :
                        raise ValueError ("Высота должна быть положительным числом")
                if not width and not height :
                    raise ValueError ("Укажите хотя бы одно измерение")
            except ValueError as e :
                messagebox .showerror (
                "Ошибка",
                f"Некорректные параметры размера: {e }"
                )
                return
        success_count =0
        error_count =0
        self .progress_var .set (0 )
        for i ,file_path in enumerate (self .files ):
            try :
                filename =os .path .basename (file_path )
                self .status_var .set (f"Конвертация {i +1 }/{len (self .files )}: {filename }")
                img =Image .open (file_path )
                if self .resize_var .get ()and (width or height ):
                    if width and height :
                        new_size =(width ,height )
                    elif width :
                        ratio =width /img .width
                        new_size =(width ,int (img .height *ratio ))
                    else :
                        ratio =height /img .height
                        new_size =(int (img .width *ratio ),height )
                    img =img .resize (new_size ,Image .LANCZOS )
                base_name =os .path .splitext (os .path .basename (file_path ))[0 ]
                output_extension =self .supported_formats [output_format ][0 ]
                output_file =os .path .join (save_path ,f"{base_name }{output_extension }")
                counter =1
                while os .path .exists (output_file ):
                    output_file =os .path .join (save_path ,f"{base_name }_{counter }{output_extension }")
                    counter +=1
                if output_format =="JPEG":
                    img .save (output_file ,format =output_format ,quality =quality )
                else :
                    img .save (output_file ,format =output_format )
                success_count +=1
                self .progress_var .set ((i +1 )/len (self .files )*100 )
            except Exception as e :
                error_count +=1
                print (f"Ошибка при конвертации {file_path }: {e }")
        if error_count ==0 :
            self .status_var .set (f"Конвертация завершена. Успешно обработано файлов: {success_count }")
            messagebox .showinfo (
            "Готово",
            f"Конвертация завершена.\nУспешно обработано файлов: {success_count }"
            )
            self ._open_folder (save_path )
        else :
            self .status_var .set (f"Конвертация завершена с ошибками. Успешно: {success_count }, ошибок: {error_count }")
            messagebox .showwarning (
            "Готово с ошибками",
            f"Конвертация завершена с ошибками.\n"
            f"Успешно обработано файлов: {success_count }\n"
            f"Ошибок: {error_count }"
            )
            self ._open_folder (save_path )
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
    def _check_dependencies (self ):
        pass