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
##
##------------------------------------------------------     
def createAppFolders():
    ##create root folder
    DirectoryScraperPath = 'C:\\DirectoryScanner\\'
    createFolder(DirectoryScraperPath)
    
    ##create today's log folder if it doesn't exist
    date = getDateNow()
    DirectoryScraperPath = 'C:\\DirectoryScanner\\'+ date +"\\"
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
##
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
##
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
##
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
##
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
##
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
##
##------------------------------------------------------ 
def searchDir(newPath,logPath):
    path = newPath
    outputPathHeader(newPath)
    for filename in os.listdir(path):
        
        ##skip folders with high level encryption and authentication,
        ##or whitelist to avoid scanning it via the skipDir(filename) function.
        if skipDir(filename) == False:
            try:
                ##if the directory doesn't have one item in it at least, skip this code
                if not len(os.listdir(path)) >=1: continue
                currentDir = os.path.join(path, filename)
                logFormattedMsg(("\n\n"+currentDir+"\n------------------------------------------"), logPath)
                
                printFileData(currentDir, filename)               
                file = prepareFile(path,filename,currentDir)
                dbFetch.checkIfExists(file,logPath)                
                dbFetch.pushFileContent(file,logPath)
               
                    ##print("failed to push content")
                          
                ##the new path is this path plus the next folder
                nextPath = os.path.join(path, filename)
                searchDir(nextPath,logPath)
                          
            except FileNotFoundError: ##skip these files when they error
                File.logFileError(file,1,logPath)
                continue
            except PermissionError:
                File.logFileError(file,2,logPath)
                continue
            except NotADirectoryError: ##just print the file's name
                if Path(currentDir).is_dir() == False : continue
                File.logFileError(file,3,logPath)
 
##------------------------------------------------------
##
##------------------------------------------------------ 
def main():
    path = 'C:\\testFileDirectories'
    run = 10
    sec = 10
    alive = True
    logPath = setOutfileInfo()
    ##goes until closed manually
    while alive == True:
        logEvent(("Scan Starting in "+ path),logPath)          
        searchDir(path,logPath)
        logEvent("Scan Finished.",logPath )
        logEvent("Moving Files for next run",logPath )        
        if run == 10:
            demo.demoMove()
            run = 11
        else:
            demo.demoReturn()
            run = 10
        time.sleep(sec)
        logEvent("Restarting scan in" + str(sec) + " seconds",logPath )
        time.sleep(sec)
##------------------------------------------------------
## Run Main program, close execution window to stop.
##------------------------------------------------------
main()
##demo.demoReturn()
##------------------------------------------------------ 

##writeFile.write(elem.firstChild.data + ",/n")       
##print(str(processed) + ' Files processed')        
##writeFile.close()

####C:\Python> python.exe "C:\Python\Scripts\DirScraper\DirectoryScanner\directoryScraper.py"
