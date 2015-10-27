from screens import *


if __name__ == "__main__":
    db = db_login_screen()

    if db:
        pass
    else:
        sys.exit(0)

    execute_file(db, "sql/available_flights.sql")
    execute_file(db, "sql/good_connections.sql")
    execute_file(db, "sql/good_three_connections.sql")
    execute_file(db, "sql/good_flights.sql")

    splash_screen(db)


    select_statement1 = "select flightno, dep_date, src, dst, to_char(dep_time,'HH24:MI'), to_char(arr_time,'HH24:MI'), fare, seats, price from available_flights order by dep_date"

    rows = db.query(select_statement1)

    for row in rows:
        print(row)
