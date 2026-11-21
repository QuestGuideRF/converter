import os
import json
class ConfigManager :
    def __init__ (self ):
        self .config_dir ="config"
        self .config_file =os .path .join (self .config_dir ,"settings.json")
        self .default_settings ={
        "theme":"light",
        "window_size":"default",
        "custom_width":900 ,
        "custom_height":600 ,
        "default_save_path":os .path .expanduser ("~/Загрузки"),
        "language":"ru",
        "recent_files":[],
        "recent_folders":[]
        }
        self .settings ={}
        self .load_settings ()
    def load_settings (self ):
        try :
            os .makedirs (self .config_dir ,exist_ok =True )
            if os .path .exists (self .config_file ):
                with open (self .config_file ,'r',encoding ='utf-8')as f :
                    self .settings =json .load (f )
            else :
                self .settings =self .default_settings .copy ()
                self .save_settings ()
        except Exception as e :
            print (f"Ошибка загрузки настроек: {e }")
            self .settings =self .default_settings .copy ()
    def save_settings (self ):
        try :
            os .makedirs (self .config_dir ,exist_ok =True )
            with open (self .config_file ,'w',encoding ='utf-8')as f :
                json .dump (self .settings ,f ,ensure_ascii =False ,indent =4 )
        except Exception as e :
            print (f"Ошибка сохранения настроек: {e }")
    def get (self ,key ,default =None ):
        return self .settings .get (key ,default )
    def set (self ,key ,value ):
        self .settings [key ]=value
        self .save_settings ()
    def reset (self ):
        self .settings =self .default_settings .copy ()
        self .save_settings ()
    def add_recent_file (self ,file_path ):
        recent_files =self .get ("recent_files",[])
        if file_path in recent_files :
            recent_files .remove (file_path )
        recent_files .insert (0 ,file_path )
        if len (recent_files )>10 :
            recent_files =recent_files [:10 ]
        self .set ("recent_files",recent_files )
    def add_recent_folder (self ,folder_path ):
        recent_folders =self .get ("recent_folders",[])
        if folder_path in recent_folders :
            recent_folders .remove (folder_path )
        recent_folders .insert (0 ,folder_path )
        if len (recent_folders )>10 :
            recent_folders =recent_folders [:10 ]
        self .set ("recent_folders",recent_folders )