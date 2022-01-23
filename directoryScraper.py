import os
from xml.dom import minidom
import time
import filetype
path = 'C:\\'
DirectoryScraper = 'C:\\DirectoryScraper\\'
outputFileExt = '.txt'
kind = filetype.guess('C:\\Microsoft\\AndroidNDK64\\android-ndk-r16b\\build\\gmsl\\gmsl\\')
print(kind)
##this can be used to set your own directory to scan manually
##path = 'C:\\'

##os.remove((DirectoryScraper+'data'+outputFileExt))
##time.sleep(0.5)

##writer = open((DirectoryScraper+'data'+outputFileExt),"w")


def searchDir(newPath):
    path = newPath
    print("\n"+path + "\\")
    print("-----------------------------")
    for filename in os.listdir(path):
        ##if the directory doesn't have one item in it at least, skip this code
        if not len(os.listdir(path)) >=1: continue
        ##my current file is this directory plus the filename in this loop
        currentDir = os.path.join(path, filename)
       
        if not '.' in filename: ##look for folders without a '.' in the file extension
            ##these directories run into access issues, skip over
            if filename == 'System Volume Information': continue 
            elif filename == 'Documents and Settings': continue
            elif filename == 'Windows': continue
            
            ##the new path is this path plus the next folder
            nextPath = os.path.join(path, filename)
            try:
                searchDir(nextPath)
            except FileNotFoundError:
                continue;     
        else:
            print(filename)
            
##while the count of files in a folder > 1 and no dot in the name:
searchDir(path)

##writeFile.write(elem.firstChild.data + ",/n")       
##print(str(processed) + ' Files processed')        
##writer.close()


####C:\Python> python.exe "C:\Python\Scripts\DirScraper\DirectoryScanner\directoryScraper.py"

