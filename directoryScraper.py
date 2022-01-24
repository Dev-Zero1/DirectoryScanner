import os
from os import scandir
from xml.dom import minidom
import time
from pathlib import Path
from datetime import datetime
import dbFetch

dbFetch.fetch()

##execfile('dbfetch.py')
path = 'C:\\'
##userInputPath= 'C:\\Microsoft\\AndroidNDK64\\android-ndk-r16b\\build\\gmsl'
DirectoryScraper = 'C:\\DirectoryScraper\\'
outputFileExt = '.txt'

##os.remove((DirectoryScraper+'data'+outputFileExt))
##time.sleep(0.5)
##writer = open((DirectoryScraper+'data'+outputFileExt),"w")

def outputPathHeader(newPath):
    print("\n"+newPath + "\\")
    print("-----------------------------")
    
def printFileData(currDir, filename):
    if not '.' in filename:                 
        print(os.listdir(currDir))                                                       
    else:
        print(filename)
        
def skipDir(filename):
    skipIndicator = False
    
    ##these directories run into access issues,
    ##skip over for now via PermissionError exception below.
    if filename == 'System Volume Information': skipIndicator = True
    elif filename == 'Documents and Settings': skipIndicator = True
    elif filename == 'Windows': skipIndicator = True
    elif filename == 'Intel': skipIndicator = True
    elif filename == 'Microsoft': skipIndicator = True
    return skipIndicator

def searchDir(newPath):
    path = newPath
    outputPathHeader(newPath)
    for filename in os.listdir(path):
        
        ##skip folders with high level encryption and authentication,
        ##or whitelist to avoid scanning it via the skipDir(filename) function.
        if skipDir(filename) == False:
            try:
                ##if the directory doesn't have one item in it at least, skip this code
                if not len(os.listdir(path)) >=1: continue            
                ##my current file is this directory plus the filename in this loop
                currentDir = os.path.join(path, filename)
                printFileData(currentDir, filename)
                
                ##the new path is this path plus the next folder
                nextPath = os.path.join(path, filename)
                searchDir(nextPath)
                          
            except FileNotFoundError: ##skip these files when they error
                    continue
            except PermissionError:
                continue
            except NotADirectoryError: ##just print the file's name
                    print(filename)
                    continue
                        
##while the count of files in a folder > 1 and no dot in the name:
##searchDir(path)

##writeFile.write(elem.firstChild.data + ",/n")       
##print(str(processed) + ' Files processed')        
##writeFile.close()

####C:\Python> python.exe "C:\Python\Scripts\DirScraper\DirectoryScanner\directoryScraper.py"
