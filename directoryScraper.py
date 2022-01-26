import os
from os import scandir
from xml.dom import minidom
import time
from pathlib import Path
from datetime import datetime
import dbFetch
import File

path = 'C:\\'
DirectoryScraper = 'C:\\DirectoryScraper\\'
outputFileExt = '.txt'


def outputPathHeader(newPath):
    print("\n"+newPath + "\\")
    print("-----------------------------")
    
def printFileData(currDir, filename):
    if not '.' in filename:                 
        print(os.listdir(currDir))                                                       
    else:
        print(filename)
        
def getFileType(filename):
    fType = ''
    if not '.' in filename:                 
        fType = 'folder'                                                     
    else:
        try:
            fType = filename.rsplit('.', 1)[1]
        except IndexError:
             fType = 'unknown'
    return fType
        
def skipDir(filename):
    skipIndicator = False
    
    ##these directories run into access issues,
    ##skip over for now via PermissionError exception below.
    if filename == 'System Volume Information': skipIndicator = True
    elif filename == 'Documents and Settings': skipIndicator = True
    elif filename == 'Windows': skipIndicator = True
    elif filename == 'Intel': skipIndicator = True
    elif filename == 'Microsoft': skipIndicator = True
    elif filename == '$Recycle.Bin': skipIndicator = True
    return skipIndicator

def getFileId():
    fID = 0
    fID = dbFetch.fetch("SELECT fileId from files order by fileId desc limit 1")
    try:
        fID = fID[0][0] + 1
    except IndexError:
        fID = 1
    return fID

def prepareFile(path,filename,currentDir):   
    fType = getFileType(filename)
    fSize = os.path.getsize(currentDir)
    fLastMod = datetime.fromtimestamp(os.path.getmtime(currentDir)).strftime('%Y-%m-%d-%H:%M')
    fCreated = datetime.fromtimestamp(os.path.getctime(currentDir)).strftime('%Y-%m-%d-%H:%M')
    timeNow  = dbFetch.fetch("select now()")
    timeNow = timeNow[0][0]
    
    fID = getFileId()
    file = File.make_file(int(fID), filename, path, fType,fLastMod,fCreated,timeNow, int(fSize))
    return file

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
                file = prepareFile(path,filename,currentDir)
                dbFetch.push(file)
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
def main():
    sec = 20
    alive = True
    ##while the count of files in a folder > 1 and no dot in the name:
    while alive == True:
        print("Scan Starting." )
        searchDir(path)
        print("Scan Finished." )
        print("Restarting scan in" + str(sec) + " seconds" )
        time.sleep(sec)
        
     
main()
##writeFile.write(elem.firstChild.data + ",/n")       
##print(str(processed) + ' Files processed')        
##writeFile.close()

####C:\Python> python.exe "C:\Python\Scripts\DirScraper\DirectoryScanner\directoryScraper.py"
