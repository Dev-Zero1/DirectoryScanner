class File(object):
    fileID = 0
    fileName = ""
    fileDir = ""
    fileType = ""
    fileLastModified = ""
    fileSize = 0
            
    def __init__(self,fID, fName, fDir, fType,fLastMod,fSize):
        self.fileID = fID
        self.name = fName
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
