    # -*- coding: utf-8 -*-

import shutil
import os
import glob
import _thread
from tkinter import *
from tkinter import filedialog
from time import time

class Arrangement:
    def __init__(self,folder_path):
        self.folder_path = folder_path
        
        self.music = ['mp3','wav','aac','m4a','m4b','ogg','wma','aif']
        self.images = ['jpg','png','jpeg','gif','tiff','psd','eps','ai','indd','raw','svg','webp','ico','tif','bmp','ps']
        self.videos = ['webm','mpg','mp2','mpeg','mpe','mp4','m4p','m4v','avi','wmv','mov','qt','flv','swf','avchd','vob','rm','mkv','h264','3gp']         
        self.docs = ['odt','pdf','rtf','tex','txt','wpd','doc','docx']
        self.spreadsheets = ['ods','xlsm','xlsm','xlsx','csv']
        self.archives = ['zip','tar','7z','arj','deb','pkg','rar','rpm','tar.gz','z','bin','dmg','iso','toast','vcd']
        self.apps = ['apk','bat','bin','cgi','pl','com','exe','gadget','jar','msi','wsf']
        self.presentations=['ppt','.pptx','pptm','potx','key','odp','pps']
        self.programming=['c','cpp','cgi','pl','class','py','cs','h','java','php','sh','swift','vb']

    def magic_code(self,folder_path,format_list,folder_type):

        file_list=[]
        for extenstion in format_list:    
            files = [file for file in glob.glob(folder_path+"**/*."+extenstion,recursive=True)]  
            files1 = [file for file in glob.glob(folder_path+"**/*."+extenstion.upper(),recursive=True)]  
            file_list.extend(files)
            file_list.extend(files1)
            
        if not len(file_list)==0:
            if not os.path.isdir(folder_path+'/'+folder_type):
                os.makedirs(folder_path+'/'+folder_type)   
            for f in file_list:
                shutil.move(f,folder_path+'/'+folder_type)
        return 'Process done'
    
    def arranging_files(self):
        files=os.listdir(self.folder_path)
        if len(files) == 0:
            return 'Folder is empty.'
        else:
            _thread.start_new_thread(self.magic_code, (self.folder_path,self.images,'Images'))
            _thread.start_new_thread(self.magic_code, (self.folder_path,self.videos,'Videos'))
            _thread.start_new_thread(self.magic_code, (self.folder_path,self.docs,'Docs'))
            _thread.start_new_thread(self.magic_code, (self.folder_path,self.music,'Music'))
            _thread.start_new_thread(self.magic_code, (self.folder_path,self.spreadsheets,'Spreadsheets'))
            _thread.start_new_thread(self.magic_code, (self.folder_path,self.archives,'Archives'))
            _thread.start_new_thread(self.magic_code, (self.folder_path,self.apps,'Applications and Executables'))
            _thread.start_new_thread(self.magic_code, (self.folder_path,self.presentations,'Presentations'))
            _thread.start_new_thread(self.magic_code, (self.folder_path,self.programming,'Programming Files'))
            
#            handeling other files which does not lie in any of the above category
            files=os.listdir(self.folder_path)
            if len(files) != 0:
                if not os.path.isdir(self.folder_path+'/'+'Others'):
                    os.makedirs(self.folder_path+'/'+'Others')   
                for f in files:
                    if os.path.isfile(f):
                        shutil.move(f,self.folder_path+'/'+'Others')

            return 'Process Done'
            
    def trigger_func(self):
        if os.path.isdir((self.folder_path)):
            j=self.arranging_files()
            return j
        else:
            return 'Invalid folder is selected'


#UI elements
def run_UI():  	
    
    def browseFiles():
        try:
            st=time()
            folder_path = filedialog.askdirectory(initialdir = "/Downloads")
            label_after_selection.configure(text="Selected Folder: "+folder_path)
            pathlabel.configure(text="File Arragement is in Process please wait")
            obj = Arrangement(str(folder_path))
            obj.trigger_func()
            et = time()
            pathlabel.configure(text="File organized in "+str(round(et-st,4))+" seconds",fg = "black")
        except:
            pathlabel.configure(text="Some error occured. Please try again.",fg = "red")
        

    
																								
    window = Tk()
    
    window.title('File Organizer by Lazzzy Coder')
    
    window.geometry("600x400+400+200")
    
    window.config(background = "purple")
    photo=PhotoImage(file="lazylogo.gif")
    Label(window,bg='purple').pack(pady=5)

    Label(window,image=photo,bg='purple').pack(pady=5)
    
    Label(window,
            text = "Select the folder by by clicking the browse button below.",
            width = 100, height = 2,
            font='Times 16 bold',bg='purple',
            fg = "white").pack(pady=5)
    
    
    Button(window,
            text = "Browse Files",
            width= 20,height=2,
            bg='white',fg='purple',
            font='Helvetica 12 bold italic',
            command = browseFiles).pack(pady=5)
    
    label_after_selection = Label(window,
    							text = "Selected Folder: None ",
    							width = 100, height =2,
                                font='Times 14 bold',
    							fg = "white",bg='purple')
    
    label_after_selection.pack(pady=5)
    
    
    pathlabel = Label(window,fg = "red",bg='purple',font='Times 16 italic bold')
    pathlabel.pack(pady=5)

    window.mainloop()

#calling the main function
    
if __name__ == "__main__":
    st=time()
    p=run_UI()
    end=time()
    print("App closed in ",round(end-st,3)," seconds")
    

