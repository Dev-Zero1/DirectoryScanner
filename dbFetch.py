import File

def setCredentials():
  credFile = 'C:\\Python\\Scripts\\sqlData\\sqlInfo.csv'
  ##this file has my username and password separated by comma
  ##aids in keeping my credentials for the database off the github repo
  with open(credFile, mode ='r')as myFile:
    lines = myFile.readlines()
    lines = lines[0].split(",")
    return lines

def fetch():
   
  import mysql.connector
  credentials = setCredentials()
  
  db = mysql.connector.connect(
    host="localhost",
    user=credentials[0],
    password=credentials[1],
    database="directoryScanner"
  )

  mc = db.cursor()
  
  mc.execute("SELECT * FROM files")
  result = mc.fetchall()
  f = File.make_blankFile()
  
  for row in result:
    f.fileID = row[0]
    f.fileName = str(row[1])
    f.fileDir = str(row[2])
    f.fileType = str(row[3])
    f.fileLastModified = str(row[4])
    f.fileSize = str(row[5])

##  command = "INSERT INTO files VALUES (%d,%s, %s, %s,%s,%d)"
##  values = (f.fileID, f.fileName,f.fileDir,f.fileType,f.fileLastModified,f.fileSize)
##  mc.execute(command, values)
##  db.commit()
##
##  print(mc.rowcount, "record successfully inserted.")
    
    
    print(row[1]) ##fileName
    print("---------------------")
    print(row[2])##fileDir
    print(row[3])##fileType
    print(row[4])##fileLastModified
    print(str(row[5])+'\n')##fileSize


