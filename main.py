# Note: Python does not have an auto commit. Thus, commit at the end of each statement is important.
# python3 CreateToffees.py
# File from introduction to cx_oracle



import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it
import gui.easygui as ui



def createTable(connection):

  dropTables = ["drop table airline_agents","drop table bookings","drop table tickets","drop table passengers","drop table users","drop table flight_fares","drop table fares","drop table sch_flights","drop table flights","drop table airports"]
  createTables = ["create table airports (acode char(3), name char(30), city char(15), country char(15), tzone int, primary key (acode))",
          "create table flights (flightno char(6),src char(3),dst char(3),dep_time date,est_dur int, primary key (flightno),foreign key (src) references airports, foreign key (dst) references airports)",
          "create table sch_flights (flightno char(6),dep_date  date,act_dep_time date,act_arr_time date,primary key (flightno,dep_date),foreign key (flightno) references flights on delete cascade)",
          "create table fares (fare char(2),descr char(15),primary key (fare))",
          "create table flight_fares (flightno  char(6),fare char(2),limit int,price float,bag_allow int,primary key (flightno,fare),foreign key (flightno) references flights,foreign key (fare) references fares)",
          "create table users (email char(20),pass char(4),last_login  date,primary key (email))",
          "create table passengers (email char(20),name char(20),country  char(10),primary key (email,name))",
          "create table tickets (tno int,name char(20),email char(20),paid_price float,primary key (tno),foreign key (email,name) references passengers)",
          "create table bookings (tno int,flightno  char(6),fare char(2),dep_date date,seat char(3),primary key (tno,flightno,dep_date),foreign key (tno) references tickets,foreign key (flightno,dep_date) references sch_flights,foreign key (fare) references fares)",
          "create table airline_agents (email char(20),name char(20),primary key (email),foreign key (email) references users)"]

  try:
    curs = connection.cursor()
    
    with open("data.sql", "r") as datafile:
      data = []
      for line in datafile:
          data.append(line.replace('\n', '').replace(';', ''))

    for cmd in dropTables:
      curs.execute(cmd)

    for cmd in createTables:
      curs.execute(cmd)

    for cmd in data:
      curs.execute(cmd)
    connection.commit()
    curs.close()
    

  except cx_Oracle.DatabaseError as exc:
    ui.msgbox(exc.args[0],"Error")
    
def dbLogin():
  msg = "Enter Oracle Connection Information"
  title = "Connect to Oracle"
  fieldNames = ["Host", "Port", "SID","Username", "Password"]
  fieldValues = ["localhost", "1525", "crs","jutt", "ps3hammad"]
  errmsg = ""

  while 1:
    fieldValues = ui.multpasswordbox(errmsg, title, fieldNames, fieldValues)
    if fieldValues == None: break
    errmsg = ""
    for i in range(len(fieldNames)):
      if fieldValues[i].strip() == "":
        errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
    conString=''+fieldValues[3]+'/' + fieldValues[4] +'@'+fieldValues[0]+':'+fieldValues[1]+'/'+fieldValues[2]
    if errmsg == "":
      try:
        connection = cx_Oracle.connect(conString)
        return connection # no problems found
      except cx_Oracle.DatabaseError as exc:
        ui.msgbox(exc.args[0],"Error")
  
def loginRegister(connection):
  lMsg = "Login to Flight Finder"
  lTitle = "Login"
  rMsg = "Register for Flight Finder"
  rTitle = "Register"
  fieldNames = ["Email", "Password"]
  

  while 1:

    fieldValues = []
    choice = ui.indexbox("Welcome to Flight Finder", "Login/Register",['Login', 'Register','Exit'])

    if choice == 0:
      #login
      errmsg = lMsg
      while 1:
        fieldValues = ui.multpasswordbox(errmsg, lTitle, fieldNames, fieldValues)
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
          if fieldValues[i].strip() == "":
            errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        email = fieldValues[0]
        pwd = fieldValues[1]
        if errmsg == "":
          try:
            #Check that user is in database and password is correct
            return email
          except cx_Oracle.DatabaseError as exc:
            ui.msgbox(exc.args[0],"Error")
      continue
    elif choice == 1:
      #register
      errmsg = rMsg
      while 1:
        fieldValues = ui.multpasswordbox(errmsg, rTitle, fieldNames, fieldValues)
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
          if fieldValues[i].strip() == "":
            errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        email = fieldValues[0]
        pwd = fieldValues[1]
        if errmsg == "":
          try:
            #Check that user is not in database and password is 4 char
            return email
          except cx_Oracle.DatabaseError as exc:
            ui.msgbox(exc.args[0],"Error")
      continue
    else:
      #exit
      sys.exit(0)


if __name__ == "__main__":
  connection = dbLogin()
  if connection:
    pass
  else:
    sys.exit(0)

  createTable(connection)
  print(loginRegister(connection))

  connection.close()
