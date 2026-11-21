import os
import shutil
import mimetypes
from pathlib import Path
def get_file_size (file_path ,human_readable =True ):
    size_bytes =os .path .getsize (file_path )
    if not human_readable :
        return size_bytes
    for unit in ['B','KB','MB','GB','TB']:
        if size_bytes <1024.0 :
            return f"{size_bytes :.2f} {unit }"
        size_bytes /=1024.0
    return f"{size_bytes :.2f} PB"
def get_file_type (file_path ):
    mime_type ,_ =mimetypes .guess_type (file_path )
    if mime_type :
        return mime_type
    else :
        _ ,ext =os .path .splitext (file_path )
        if ext :
            return f"Unknown type ({ext })"
        else :
            return "Неизвестный тип"
def is_supported_image (file_path ):
    supported_extensions =['.jpg','.jpeg','.png','.gif','.bmp','.tiff','.webp','.ico']
    _ ,ext =os .path .splitext (file_path )
    return ext .lower ()in supported_extensions
def is_supported_document (file_path ):
    supported_extensions =['.pdf','.docx','.doc','.txt','.rtf','.odt','.html','.htm','.md','.markdown']
    _ ,ext =os .path .splitext (file_path )
    return ext .lower ()in supported_extensions
def is_supported_audio (file_path ):
    supported_extensions =['.mp3','.wav','.ogg','.flac','.aac','.m4a','.wma']
    _ ,ext =os .path .splitext (file_path )
    return ext .lower ()in supported_extensions
def is_supported_video (file_path ):
    supported_extensions =['.mp4','.avi','.mkv','.mov','.wmv','.flv','.webm']
    _ ,ext =os .path .splitext (file_path )
    return ext .lower ()in supported_extensions
def is_supported_archive (file_path ):
    supported_extensions =['.zip','.rar','.7z','.tar','.gz','.bz2']
    _ ,ext =os .path .splitext (file_path )
    return ext .lower ()in supported_extensions
def ensure_dir (directory ):
    if not os .path .exists (directory ):
        os .makedirs (directory ,exist_ok =True )
def copy_file (source ,destination ):
    try :
        shutil .copy2 (source ,destination )
        return True
    except Exception as e :
        print (f"Ошибка копирования файла: {e }")
        return False
def get_unique_filename (output_path ):
    if not os .path .exists (output_path ):
        return output_path
    directory ,filename =os .path .split (output_path )
    name ,ext =os .path .splitext (filename )
    counter =1
    while os .path .exists (output_path ):
        output_path =os .path .join (directory ,f"{name }_{counter }{ext }")
        counter +=1
    return output_path
def get_icon_path ():
    root_dir =os .path .dirname (os .path .dirname (os .path .abspath (__file__ )))
    icon_path =os .path .join (root_dir ,"converter.ico")
    if os .path .exists (icon_path ):
        return icon_path
    return None
def get_file_extension (file_path ):
    return os .path .splitext (file_path )[1 ].lower ()