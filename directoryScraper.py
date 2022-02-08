##------------------------------------------------------##
##
##------------------------------------------------------##
import os
##from os import scandir
##from xml.dom import minidom
import time
from pathlib import Path
from datetime import datetime
import dbFetch
import File
import demo
import sys
from tkinter import messagebox

##------------------------------------------------------
##showNotification() pops up a message of the string arg
##------------------------------------------------------  
def showNotification(notice):
    messagebox.showinfo('Information',notice)
##------------------------------------------------------
##getDateNow() returns a string date of
##YYYYMMDD or '20220129' if Jan 29, 2022
##------------------------------------------------------    
def getDateNow():
    timeNow  = dbFetch.fetch("select now()")    
    date = str(timeNow[0][0]).replace('-','')[:8]
    return date
##------------------------------------------------------
##getLogDateNow returns a string date UTC of
##YYYY-MM-DD HH:MM: or  '2022-01-29 10:50:37' if Jan 29, 2022
##------------------------------------------------------ 
def getLogDateTime():
    timeNow  = dbFetch.fetch("select now()")    
    date = str(timeNow[0][0])
    return date
##------------------------------------------------------
##logEvent writes to the log folder in
##C:\DirectoryScraper\YYYYMMDD\DirScraperLog.txt
##------------------------------------------------------ 
def logEvent(msg, logPath):
    logWriter = open(logPath,"a")   
    msg = "\n" +str(getLogDateTime())+" EventLogged: "+msg 
    logWriter.write(msg + "\n")
    logWriter.close()

def logFormattedMsg(msg, logPath):
    logWriter = open(logPath,"a")   
    logWriter.write(msg)
    logWriter.close()
##------------------------------------------------------
##initialization for creating the application folders and logs
##------------------------------------------------------     
def createAppFolders():
    ##create root folder
    DirectoryScraperPath = 'C:\\DirectoryScanner\\'
    createFolder(DirectoryScraperPath)
    
    DirectoryScraperLogPath = 'C:\\DirectoryScanner\\DS_Logs\\'
    createFolder(DirectoryScraperLogPath)
    
    ##create today's log folder if it doesn't exist
    date = getDateNow()
    DirectoryScraperPath = 'C:\\DirectoryScanner\\DS_Logs\\'+ date +"\\"
    createFolder(DirectoryScraperPath)
    
    ##create today's log file if it doesn't exist
    fileExt = '.txt'
    logName = 'DirScannerLog'+ fileExt
    logPath = DirectoryScraperPath+logName
    createFile(logPath)
    return logPath

def setOutfileInfo():              
    logPath = createAppFolders()    
    return logPath

def createFolder(path):
    if not os.path.exists(path):
        os.mkdir(path)
        
def createFile(path):
    if not os.path.exists(path):
        os.system('touch '+path)
##------------------------------------------------------
##console output for file scans
##------------------------------------------------------         
def outputPathHeader(newPath):
    print("\n\n"+newPath + "\\")
    print("-----------------------------")
    
def printFileData(currDir, filename):
    if not '.' in filename:                 
        print(os.listdir(currDir))                                                       
    else:
        print(filename)
##------------------------------------------------------
##parses the file type from the filename
##returns the extension "exe", "txt", etc.
##------------------------------------------------------         
def getFileType(currDir,filename):
    fType = ''
    if Path(currDir).is_dir():                 
        fType = 'folder'                                                     
    else:
        try:
            fType = filename.rsplit('.', 1)[1]
        except IndexError:
             fType = 'unknown'
    return fType
##------------------------------------------------------
##allows the program to avoid useless/blocked directories
##------------------------------------------------------         
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
    elif filename == 'DirectoryScanner': skipIndicator = True
    return skipIndicator
##------------------------------------------------------
##fetches the most current fileId to use for the DB insert
##------------------------------------------------------ 
def getFileId():
    fID = 0
    fID = dbFetch.fetch("SELECT fileId from files order by fileId desc limit 1")
    try:
        fID = fID[0][0] + 1
    except IndexError:
        fID = 1
    return fID
##------------------------------------------------------
##prepares a file object with the scanned data to return
##------------------------------------------------------ 
def prepareFile(path,filename,currentDir):   
    fType = getFileType(currentDir,filename)
    fSize = os.path.getsize(currentDir)
    
    fLastMod = datetime.fromtimestamp(os.path.getmtime(currentDir)).strftime('%Y-%m-%d-%H:%M')
    fLastMod = fLastMod[:10] +' '+fLastMod[11:]+":00"
    
    fCreated = datetime.fromtimestamp(os.path.getctime(currentDir)).strftime('%Y-%m-%d-%H:%M')
    fCreated = fCreated[:10] +' '+fCreated[11:]+":00"
    
    timeNow  = dbFetch.fetch("select now()")
    timeNow = timeNow[0][0]
    
    fID = getFileId()
    file = File.make_file(int(fID), filename, path, fType,fLastMod,fCreated,timeNow, int(fSize))
    return file
##------------------------------------------------------
##Recursive function to scan over each directories contents
##checks for duplication
##commits files with different lastModified signatures
##commits folders with different directory signatures.
##------------------------------------------------------ 
def searchDir(newPath,logPath):
    path = newPath
    outputPathHeader(newPath)
    for filename in os.listdir(path):   
        ##skip folders with high level encryption and authentication,
        ##or whitelist to avoid scanning it via the skipDir(filename) function.
        if skipDir(filename) == False:
            try:
                ##if the directory has at least one item in it, run this code
                if len(os.listdir(path)) >=1:
                    currentDir = os.path.join(path, filename)
                    logFormattedMsg(("\n\n"+currentDir+"\n------------------------------------------"), logPath)
                    
                    printFileData(currentDir, filename)               
                    file = prepareFile(path,filename,currentDir)
                    dbFetch.checkIfExists(file,logPath)                
                    dbFetch.pushFileContent(file,logPath)
                                          
                    ##the new path is this path plus the next folder
                    nextPath = os.path.join(path, filename)
                    searchDir(nextPath,logPath)                          
            except FileNotFoundError: ##skip these files when they error
                File.logFileError(file,1,logPath)              
            except PermissionError:
                File.logFileError(file,2,logPath)           
            except NotADirectoryError: 
                if Path(currentDir).is_dir() == True:
                    File.logFileError(file,3,logPath)
##------------------------------------------------------
##
##----------------------------------------------------                
def validateFile(newPath, filename, logPath):
    path = newPath
    outputPathHeader(filename)        
        ##skip folders with high level encryption and authentication,
        ##or whitelist to avoid scanning it via the skipDir(filename) function.
    if skipDir(filename) == False:
        try:
            print(path+filename)
            ##if the directory and path file exist, run this code
            if os.path.exists(path+filename):               
                currentDir = os.path.join(path, filename)
                logFormattedMsg(("\n\n"+currentDir+"\n------------------------------------------"), logPath)                
                printFileData(currentDir, filename)               
                file = prepareFile(path,filename,currentDir)
                dbFetch.checkIfExists(file,logPath)                
                dbFetch.pushFileContent(file,logPath)                        
        except FileNotFoundError: ##skip these files when they error
            File.logFileError(file,1,logPath)
        except PermissionError:
            File.logFileError(file,2,logPath)
        except NotADirectoryError: ##just print the file's name
            if Path(currentDir).is_dir() == True: 
                File.logFileError(file,3,logPath)
 
##------------------------------------------------------
## main runs in 3 modes:
##scanDir   -   scans a single directory once, notifies when finished.
##scanFile  -   scans a file once, notifies when finished.
##auto      -   scans a directory repeatedly, monitoring for changes.
##------------------------------------------------------ 
def main():
    args = sys.argv[1:]
    print(args)
    path = args[0]
    filename = args[1]
    mode = args[2]
    logPath = setOutfileInfo()
    ##sec == args[3] NOT IMPLEMENTED, scan interval time could be set during runtime.
    
    if mode == "scanDir":
        logEvent(("Scan Starting in "+ path),logPath)
        searchDir(path,logPath)
        logEvent("Scan Finished.",logPath )
        showNotification(('Scan Finished for folder :\n' + path)) 
    elif mode == "scanFile":
        logEvent(("Scan Starting in "+ path),logPath)
        validateFile(path, filename, logPath)
        logEvent(("Scan Finished for file "+ path),logPath )
        if filename != 'DS_Logins.txt':
            showNotification(('Scan Finished in :\n' + path))
    elif mode == "auto":
        alive = True
        sec = 5
        while alive == True:     
            logEvent(("Scan Starting in "+ path),logPath)
            searchDir(path,logPath)
            logEvent(("Scan Finished in "+ path +"\nStarting again in " + str(sec) + " seconds."),logPath )
            time.sleep(sec)

##------------------------------------------------------
## Run Main program
##------------------------------------------------------
main()  
##------------------------------------------------------ 


##def mainTest():
##  
##    path = 'C:\\inetpub\\'
##    mode = 'scanDir'
##    filename = ''
##    logPath = setOutfileInfo()
##    print("path =" + path)
##    print("filename =" + filename)
##    print("mode=" + mode)
##    logEvent(("Scan Starting in "+ path),logPath)
##    if mode == "scanDir":
##        searchDir(path,logPath)
##    elif mode == "scanFile":
##      validateFile(path, filename, logPath)
##    logEvent("Scan Finished.",logPath )
##
##import zipfile
##with zipfile.ZipFile(zipPath, 'r') as zip:
##    zip.extractall(dirPath)

####C:\Python> python.exe "C:\Python\Scripts\DirScraper\DirectoryScanner\directoryScraper.py"
