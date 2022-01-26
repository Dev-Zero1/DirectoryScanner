class File(object):
    fileID = 0
    fileName = ""
    fileDir = ""
    fileType = ""
    fileLastModified = ""
    fileCreated = ""
    fileSize = 0
            
    def __init__(self,fID, fName, fDir, fType,fLastMod, fCreate,fSize):
        self.fileID = fID
        self.fileName = fName
        self.fileDir = fDir
        self.fileType = fType
        self.fileLastModified = fLastMod
        self.fileCreated = fCreate
        self.fileSize = fSize


def make_file(fID, fName, fDir, fType,fLastMod,fCreate,fSize):
    file = File(fID, fName, fDir, fType,fLastMod,fCreate,fSize)
    return file

def make_blankFile():
    file = File(0,"","","","","",0)
    return file

def displayFile(file):
    print(file.fileName)
    print("---------------------")
    print("ID\t\t"+file.fileID)
    print("Dir\t\t"+file.fileDir)
    print("Type\t\t"+file.fileType)
    print("LastMod\t\t"+file.fileLastModified)
    print("Created\t\t"+file.fileCreated)
    print("Size\t\t"+file.fileSize)

