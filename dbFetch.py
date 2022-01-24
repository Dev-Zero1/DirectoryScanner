import File

def setCredentials():
  credFile = 'C:\\Python\\Scripts\\sqlData\\sqlInfo.csv'

  with open(credFile, mode ='r')as myFile:
    lines = myFile.readlines()
    lines = lines[0].split(",")
    return lines

def fetch():
  file = File.make_blankFile() 
  import mysql.connector
  credentials = setCredentials()
  
  db = mysql.connector.connect(
    host="localhost",
    user=credentials[0],
    password=credentials[1],
    database="directoryScanner"
  )

  mc = db.cursor()
  
##
##  command = "INSERT INTO files VALUES (%d,%s, %s, %s,%s,%d)"
##  values = ("John", "Highway 21")
##  mc.execute(command, values)
##
##  db.commit()
##
##  print(mc.rowcount, "record successfully inserted.")



  mc.execute("SELECT * FROM files")
  result = mc.fetchall()

  for row in result:
      print(row[1])
      print("---------------------")
      print(row[2])
      print(row[3])
      print(row[4])
      print(str(row[5])+'\n')


