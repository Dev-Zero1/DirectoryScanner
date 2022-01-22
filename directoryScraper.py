import os
from xml.dom import minidom
import time

path = 'C:\\'
DirectoryScraper = 'C:\\DirectoryScraper\\'
outputFileExt = '.txt'
##this can be used to set your own directory to scan manually
##path = 'C:\\'

##os.remove((DirectoryScraper+'data'+outputFileExt))
##time.sleep(0.5)

##writer = open((DirectoryScraper+'data'+outputFileExt),"w")


def searchDir(path):
    for filename in os.listdir(path):
        ##if not len(os.listdir(path)) >1: continue
        currentDir = os.path.join(path, filename)
        print('\n\n'+currentDir)
        print("-----------------------------")        
        if not '.' in currentDir:
            if filename == 'System Volume Information': continue ##these two directories run into access issues, skip over
            elif filename == 'Documents and Settings': continue
            path = os.path.join(path, filename)        
            try:
                for filename in os.listdir(path):
                    nextFile = os.path.join(path, filename)
                    print(nextFile)
                path = os.path.dirname(path)
            except:
                print('\nError reading '+ path)            
        else:
            print(filename)
            
##while the count of files in a folder > 1 and no dot in the name:
searchDir(path)

##    
##for filename in os.listdir(path):
##    currentDir = os.path.join(path, filename)
##    print('\n\n'+currentDir)
##    print("-----------------------------")
##    if not '.' in currentDir:
##        if filename == 'System Volume Information': continue ##these two directories run into access issues, skip over
##        elif filename == 'Documents and Settings': continue
##        path = os.path.join(path, filename)        
##        try:
##            for filename in os.listdir(path):
##                nextFile = os.path.join(path, filename)
##                print(nextFile)
##            path = os.path.dirname(path)
##        except:
##            print('\nError reading '+ path)            
##    else:
##        print(filename)  
        

    
   
    

##writeFile.write(elem.firstChild.data + ",/n")       
##print(str(processed) + ' Files processed')        
##writer.close()
