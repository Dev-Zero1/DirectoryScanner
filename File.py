##------------------------------------------------------##
##
##------------------------------------------------------##
class File(object):
    fileID = 0
    fileName = ""
    fileDir = ""
    fileType = ""
    fileLastModified = ""
    fileCreated = ""
    timeNow = ""
    fileSize = 0
            
    def __init__(self,fID, fName, fDir, fType,fLastMod, fCreate, tNow, fSize):
        self.fileID = fID
        self.fileName = fName
        self.fileDir = fDir
        self.fileType = fType
        self.fileLastModified = fLastMod
        self.fileCreated = fCreate
        self.timeNow = tNow
        self.fileSize = fSize
        
##------------------------------------------------------
##This format function returns a path directory for foldersthat always ends in '\'
##------------------------------------------------------
def formatCurrentDir(path):
    if(path[len(path)-1] == '\\'):
      return path
    else:
        path = path + '\\'
    return path
##------------------------------------------------------
##
##------------------------------------------------------        
def make_file(fID, fName, fDir, fType,fLastMod,fCreate,tNow, fSize):
    file = File(fID, fName, fDir, fType,fLastMod,fCreate,tNow, fSize)
    return file

def make_blankFile():
    file = File(0,"","","","","","",0)
    return file
##------------------------------------------------------
##
##------------------------------------------------------
def displayFile(file):
    print(file.fileName)
    print("---------------------")
    print("ID\t\t"+str(file.fileID))
    print("Dir\t\t"+file.fileDir)
    print("Type\t\t"+file.fileType)
    print("LastMod\t\t"+file.fileLastModified)
    print("Created\t\t"+file.fileCreated)
    print("TimeNow\t\t"+str(file.timeNow))
    print("Size\t\t"+str(file.fileSize))

def formatFileDir(self):
    if self.fileDir[len(self.fileDir)-1] !='\\':
        return (self.fileDir + '\\')
    else:
        return self.fileDir
##------------------------------------------------------
##
##------------------------------------------------------
def logFileError(self, errType, logPath):  
    logWriter = open(logPath,"a")   
    errMsg = ""

    if errType == 1:    errMsg = "\n" + str(self.timeNow) + "(FileNotFoundError): " + formatFileDir(self) + self.fileName
    elif errType == 2:  errMsg = "\n" + str(self.timeNow) + "(PermissionError): " + formatFileDir(self) +  self.fileName
    elif errType == 3:  errMsg = "\n" + str(self.timeNow) + "(NotADirectoryError): " + formatFileDir(self) +  self.fileName
    else:               errMsg = "\n" + str(self.timeNow) + "(Unknown Error): " + formatFileDir(self) +  self.fileName
        
    logWriter.write(errMsg)
    logWriter.close()
##------------------------------------------------------
##
##------------------------------------------------------    
def logError(self, errMsg, logPath):
    logWriter = open(logPath,"a")   
    errMsg =  "\n" +str(self.timeNow) + " " + errMsg ##+ " --- on file " + formatFileDir(self) + self.fileName
    logWriter.write(errMsg)
    logWriter.close()
