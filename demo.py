##functions to move files after the first scan.
import os
import shutil

def moveFiles(CU):
    sourceDir = f'C:\\testFileDirectories\\{CU}\\currentFolder'
    targetDir = f'C:\\testFileDirectories\\{CU}\\moveFolder'
    
    fileNames = os.listdir(sourceDir)
    
    for file in fileNames:
        shutil.move(os.path.join(sourceDir, file), targetDir)

def returnFiles(CU):
    sourceDir = f'C:\\testFileDirectories\\{CU}\\moveFolder'
    targetDir = f'C:\\testFileDirectories\\{CU}\\currentFolder'
    
    fileNames = os.listdir(sourceDir)
    
    for file in fileNames:
        shutil.move(os.path.join(sourceDir, file), targetDir)
        
def demoMove():
    moveFiles("MYCU")   
    moveFiles("EXCU")
    moveFiles("ECCU")
    moveFiles("CCCU")
    moveFiles("TRYCU")
    print('Move finished for test files from Current to Move folder.')
    
def demoReturn():
    returnFiles("MYCU")   
    returnFiles("EXCU")
    returnFiles("ECCU")
    returnFiles("CCCU")
    returnFiles("TRYCU")
    print('Move finished for test files from Move to Current folder.')
