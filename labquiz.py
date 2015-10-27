from screens import *


def q1(db):
    while True:
        fieldNames = ["Min Price", "Max Price"]
        input = formPrompt("Enter a min and max price for laptops", "Laptops", fieldNames, 0)
        if input is None:
            sys.exit(0)

        query1 = "SELECT model FROM c291.laptop WHERE price >= {} AND price <= {} ORDER BY price".format(int(input[0]),int(input[1]))
        rows = db.query(query1)
        result = "Model Numbers: "
        for row in rows:
            result += str(row[0]) + ", "

        ui.msgbox(result)

        if not ui.ccbox():
            break


def q2(db):

    query2 = "SELECT * FROM c291.laptop UNION ALL SELECT * FROM c291.pc"

    db.query(query2)
    desc = db._curs.description
    cols = [d[0] for d in desc]
    primary_key = cols[0]

    create_table = "CREATE TABLE computer("
    for c in cols:
        create_table += str(c) + " CHAR(30), "
    create_table += "PRIMARY KEY ({}))".format(primary_key)


    # db.execute("DROP TABLE computer")
    db.execute(create_table)
    # db.execute("INSERT INTO computer " + query2)




db = db_login_screen()

if db:
    pass
else:
    sys.exit(0)

# q1(db)
q2(db)



