import os
import tkinter as tk
from tkinter import ttk ,filedialog ,messagebox
import threading
class DocumentConverterFrame (ttk .Frame ):
    def __init__ (self ,parent ,config ,theme ,main_window ):
        super ().__init__ (parent )
        self .parent =parent
        self .config =config
        self .theme =theme
        self .main_window =main_window
        self .supported_formats ={
        "PDF":(".pdf",),
        "DOCX":(".docx",),
        "DOC":(".doc",),
        "TXT":(".txt",),
        "RTF":(".rtf",),
        "ODT":(".odt",),
        "HTML":(".html",".htm"),
        "MARKDOWN":(".md",".markdown"),
        }
        self .conversion_map ={
        ".pdf":[".txt",".docx",".html"],
        ".docx":[".pdf",".txt",".html",".rtf",".odt"],
        ".doc":[".pdf",".txt",".docx",".html",".rtf",".odt"],
        ".txt":[".pdf",".docx",".html",".rtf",".odt"],
        ".rtf":[".pdf",".docx",".txt",".html",".odt"],
        ".odt":[".pdf",".docx",".txt",".html",".rtf"],
        ".html":[".pdf",".docx",".txt",".md"],
        ".htm":[".pdf",".docx",".txt",".md"],
        ".md":[".pdf",".docx",".html",".txt"],
        ".markdown":[".pdf",".docx",".html",".txt"],
        }
        self .files =[]
        self ._create_widgets ()
    def _create_widgets (self ):
        header =ttk .Label (self ,text ="Конвертер документов",font =("Arial",16 ,"bold"))
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
        self .format_var =tk .StringVar ()
        self .format_combobox =ttk .Combobox (
        format_frame ,
        textvariable =self .format_var ,
        state ="readonly",
        width =10
        )
        self .format_combobox .pack (side =tk .LEFT ,padx =5 )
        self .dependencies_var =tk .StringVar (
        value ="Примечание: для конвертации документов требуются дополнительные библиотеки."
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
        command =self ._convert_documents
        )
        convert_button .pack (pady =10 )
        self .progress_var =tk .DoubleVar (value =0.0 )
        self .status_var =tk .StringVar (value ="")
        self ._check_dependencies ()
    def _check_dependencies (self ):
        missing_libs =[]
        self .dependencies_var .set ("Все необходимые библиотеки установлены.")
        return
    def _add_files (self ):
        supported_extensions =[]
        for extensions in self .supported_formats .values ():
            supported_extensions .extend (extensions )
        file_types =[("Документы"," ".join (["*"+ext for ext in supported_extensions ]))]
        for format_name ,extensions in self .supported_formats .items ():
            file_types .append ((format_name ," ".join (["*"+ext for ext in extensions ])))
        file_types .append (("Все файлы","*.*"))
        files =filedialog .askopenfilenames (
        title ="Выберите документы",
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
            self ._update_available_formats ()
    def _clear_files (self ):
        self .files =[]
        self .files_listbox .delete (0 ,tk .END )
        self .status_var .set ("Список файлов очищен")
        self .format_combobox .config (values =[])
        self .format_var .set ("")
    def _remove_selected_files (self ,event =None ):
        selected_indices =self .files_listbox .curselection ()
        if not selected_indices :
            return
        for i in sorted (selected_indices ,reverse =True ):
            del self .files [i ]
            self .files_listbox .delete (i )
        self .status_var .set (f"Выбрано файлов: {len (self .files )}")
        self ._update_available_formats ()
    def _update_available_formats (self ):
        if not self .files :
            return
        file_extensions =[os .path .splitext (file )[1 ].lower ()for file in self .files ]
        available_formats =[]
        for ext in file_extensions :
            if not available_formats :
                available_formats =self .conversion_map .get (ext ,[]).copy ()
            else :
                available_formats =[fmt for fmt in available_formats if fmt in self .conversion_map .get (ext ,[])]
        format_names =[]
        for ext in available_formats :
            for format_name ,extensions in self .supported_formats .items ():
                if ext in extensions :
                    format_names .append (format_name )
                    break
        self .format_combobox .config (values =format_names )
        if format_names :
            self .format_var .set (format_names [0 ])
        else :
            self .format_var .set ("")
            self .status_var .set ("Для выбранных файлов нет доступных форматов конвертации")
    def _browse_save_path (self ):
        folder =filedialog .askdirectory (
        initialdir =self .save_path_var .get (),
        title ="Выберите папку для сохранения"
        )
        if folder :
            self .save_path_var .set (folder )
            self .config .add_recent_folder (folder )
    def _convert_documents (self ):
        if not self .files :
            self .main_window .create_dialog (
            "Нет файлов",
            "Добавьте файлы для конвертации.",
            "warning"
            )
            return
        target_format =self .format_var .get ()
        if not target_format :
            self .main_window .create_dialog (
            "Не выбран формат",
            "Выберите формат для конвертации.",
            "warning"
            )
            return
        save_path =self .save_path_var .get ()
        if not os .path .exists (save_path ):
            try :
                os .makedirs (save_path ,exist_ok =True )
            except Exception as e :
                self .main_window .create_dialog (
                "Ошибка",
                f"Не удалось создать папку для сохранения: {e }",
                "error"
                )
                return
        target_extension =self .supported_formats [target_format ][0 ]
        threading .Thread (target =self ._convert_thread ,args =(target_extension ,save_path ),daemon =True ).start ()
    def _convert_thread (self ,target_extension ,save_path ):
        success_count =0
        error_count =0
        self .progress_var .set (0 )
        for i ,file_path in enumerate (self .files ):
            try :
                filename =os .path .basename (file_path )
                self .after (0 ,lambda :self .status_var .set (f"Конвертация {i +1 }/{len (self .files )}: {filename }"))
                source_extension =os .path .splitext (file_path )[1 ].lower ()
                base_name =os .path .splitext (os .path .basename (file_path ))[0 ]
                output_file =os .path .join (save_path ,f"{base_name }{target_extension }")
                counter =1
                while os .path .exists (output_file ):
                    output_file =os .path .join (save_path ,f"{base_name }_{counter }{target_extension }")
                    counter +=1
                self ._convert_file (file_path ,output_file ,source_extension ,target_extension )
                success_count +=1
                self .after (0 ,lambda :self .progress_var .set ((i +1 )/len (self .files )*100 ))
            except Exception as e :
                error_count +=1
                print (f"Ошибка при конвертации {file_path }: {e }")
        final_success_count =success_count
        final_error_count =error_count
        if error_count ==0 :
            message =f"Конвертация завершена. Успешно обработано файлов: {success_count }"
            self .after (0 ,lambda :self .status_var .set (message ))
            self .after (0 ,lambda :self .main_window .create_dialog ("Готово",message ,"info"))
            self .after (0 ,lambda :self ._open_folder (save_path ))
        else :
            message =f"Конвертация завершена с ошибками. Успешно: {success_count }, ошибок: {error_count }"
            self .after (0 ,lambda :self .status_var .set (message ))
            self .after (0 ,lambda :self .main_window .create_dialog ("Готово с ошибками",message ,"warning"))
            self .after (0 ,lambda :self ._open_folder (save_path ))
    def _convert_file (self ,input_file ,output_file ,source_ext ,target_ext ):
        if source_ext in (".docx",".doc")and target_ext ==".pdf":
            try :
                import docx2pdf
                docx2pdf .convert (input_file ,output_file )
                return
            except ImportError :
                raise ImportError ("Для конвертации DOCX в PDF требуется библиотека docx2pdf")
        elif source_ext ==".pdf"and target_ext ==".docx":
            try :
                from pdf2docx import Converter
                cv =Converter (input_file )
                cv .convert (output_file )
                cv .close ()
                return
            except ImportError :
                raise ImportError ("Для конвертации PDF в DOCX требуется библиотека pdf2docx")
        elif source_ext ==".pdf"and target_ext ==".txt":
            try :
                import PyPDF2
                with open (output_file ,'w',encoding ='utf-8')as txt_file :
                    with open (input_file ,'rb')as pdf_file :
                        pdf_reader =PyPDF2 .PdfReader (pdf_file )
                        for page_num in range (len (pdf_reader .pages )):
                            page =pdf_reader .pages [page_num ]
                            txt_file .write (page .extract_text ())
                            txt_file .write ("\n\n")
                return
            except ImportError :
                raise ImportError ("Для конвертации PDF в TXT требуется библиотека PyPDF2")
        elif source_ext ==".txt"and target_ext ==".pdf":
            try :
                from reportlab .pdfgen import canvas
                from reportlab .lib .pagesizes import letter
                c =canvas .Canvas (output_file ,pagesize =letter )
                text =open (input_file ,'r',encoding ='utf-8').read ()
                lines =text .split ('\n')
                y =750
                line_height =14
                for line in lines :
                    if y <50 :
                        c .showPage ()
                        y =750
                    c .drawString (50 ,y ,line )
                    y -=line_height
                c .save ()
                return
            except ImportError :
                raise ImportError ("Для конвертации TXT в PDF требуется библиотека reportlab")
        elif source_ext ==".docx"and target_ext ==".txt":
            try :
                import docx
                doc =docx .Document (input_file )
                with open (output_file ,'w',encoding ='utf-8')as f :
                    for para in doc .paragraphs :
                        f .write (para .text +'\n')
                return
            except ImportError :
                raise ImportError ("Для конвертации DOCX в TXT требуется библиотека python-docx")
        elif source_ext in (".html",".htm")and target_ext ==".txt":
            try :
                from bs4 import BeautifulSoup
                with open (input_file ,'r',encoding ='utf-8')as f :
                    soup =BeautifulSoup (f .read (),'html.parser')
                    text =soup .get_text ()
                with open (output_file ,'w',encoding ='utf-8')as f :
                    f .write (text )
                return
            except ImportError :
                raise ImportError ("Для конвертации HTML в TXT требуется библиотека beautifulsoup4")
        elif source_ext in (".md",".markdown")and target_ext in (".html",".htm"):
            try :
                import markdown
                with open (input_file ,'r',encoding ='utf-8')as f :
                    md_text =f .read ()
                html =markdown .markdown (md_text )
                with open (output_file ,'w',encoding ='utf-8')as f :
                    f .write (f"<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\"utf-8\">\n</head>\n<body>\n{html }\n</body>\n</html>")
                return
            except ImportError :
                raise ImportError ("Для конвертации Markdown в HTML требуется библиотека markdown")
        raise Exception (f"Конвертация из {source_ext } в {target_ext } не поддерживается")
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