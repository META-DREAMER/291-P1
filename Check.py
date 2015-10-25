# Note: Python does not have an auto commit. Thus, commit at the end of each statement is important.
# python3 CreateToffees.py
# File from introduction to cx_oracle



import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it



def createTable():
  

  # user = raw_input("Username [%s]: " % getpass.getuser())
  # if not user:
  #   user=getpass.getuser()
  # get password
  # pw = getpass.getpass()

  user = 'jutt'
  pw = 'ps3hammad'

  conString=''+user+'/' + pw +'@localhost:1525/crs'

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
    # Establish a connection in Python
    connection = cx_Oracle.connect(conString)

    # create a cursor 
    curs = connection.cursor()
    

    # datafile = 
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
    connection.close()

  except cx_Oracle.DatabaseError as exc:
    error, = exc.args
    print( sys.stderr, "Oracle code:", error.code)
    print( sys.stderr, "Oracle message:", error.message)
    
if __name__ == "__main__":
    createTable()
