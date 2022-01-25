class File(object):
    fileID = 0
    fileName = ""
    fileDir = ""
    fileType = ""
    fileLastModified = ""
    fileSize = 0
            
    def __init__(self,fID, fName, fDir, fType,fLastMod,fSize):
        self.fileID = fID
        self.fileName = fName
        self.fileDir = fDir
        self.fileType = fType
        self.fileLastModified = fLastMod
        self.fileSize = fSize


def make_file(fID, fName, fDir, fType,fLastMod,fSize):
    file = File(fID, fName, fDir, fType,fLastMod,fSize)
    return file

def make_blankFile():
    file = File(0,"","","","",0)
    return file

def displayFile(file):
    print(file.fileName)
    print("---------------------")
    print("ID\t\t"+file.fileID)
    print("Dir\t\t"+file.fileDir)
    print("Type\t\t"+file.fileType)
    print("LastMod\t\t"+file.fileLastModified)
    print("Size\t\t"+file.fileSize)

