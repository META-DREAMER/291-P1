import sys
from utils import *
from DB import DB
from user import *


def main_screen(user):
    options = {'Search for Flights': search_screen, 'Make a Booking': make_booking_screen,
               'List Existing Bookings': bookings_screen, "Logout": logout_screen}

    if user._is_agent:
        options.update({'Record Departure': r_dept_screen, 'Record Arrival': r_arr_screen})

    choice = ui.buttonbox("Choose an option", "FlightFinder", options.keys())
    screen = options.get(choice)
    if screen is not None:
        screen(user)
    else:
        sys.exit(0)

def print_table(table):
    string = ""
    col_width = [max(len(str(x)) for x in col) for col in zip(*table)]
    for line in table:
        string += "| " + " | ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line)) + " |\n"
    return string

def search_screen(user):
    fieldNames = ["From", "Destination", "Departure Date (DD-MM-YYYY)"]
    query = formPrompt("Search for Flights (Max Two Connections)", "FlightFinder", fieldNames, 0)
    if query is None:
        main_screen(user)


    if not date_valid(query[2]):
        ui.msgbox( "Incorrect data format, should be DD-MM-YYYY", "Error")
        search_screen(user)

    date = query[2]
    src = get_acode(user._db, query[0])
    if src is None:
        ui.msgbox("No Matches for Source Airport", "Error")
        search_screen(user)
    dest = get_acode(user._db, query[1])
    if dest is None:
        ui.msgbox("No Matches for Destination Airport", "Error")
        search_screen(user)

    if ui.boolbox("Set Max Connections to 3?", "FlightFinder", default_choice='No'):
        num_stops = 2
    else:
        num_stops= 1

    if ui.boolbox("Order by connections?", "FlightFinder", default_choice='No'):
        order_by = "stops, price"
    else:
        order_by = "price"

    with open('sql/select.sql') as file:
        get_flights = file.read().replace('\n', ' ')

    flights = user._db.query(get_flights.format(src,dest,num_stops,date,order_by))
    flight_list = {}

    result_str = ""


    if flights:
        # for f in flights:
        #
        #     result="Row Num = {0}, FNO1 = {1}, FNO2 = {2}, FNO3 = {3}, Dep Date 1 = {4}, Dep Date 2 = {5}, Dep Date 3 = {6}, " \
        #            "From = {7}, To = {8}, Dep Time = {9}, Arr Time = {10}, Num Stops = {11}, Layover 1 = {12}, Layover 2 = {13}, " \
        #            "Price = {14}, Seat 1 = {15}, Fare 1 = {16}, Seat 2 = {17}, Fare 2 = {18}, " \
        #            "Seat 3 = {19}, Fare 3 = {20}".format(f[0],f[1],f[2],f[3],f[4].strftime("%d-%b-%Y"),f[5].strftime("%d-%b-%Y"),f[6].strftime("%d-%b-%Y"),
        #                                                  f[7],f[8],f[9].strftime("%H:%M"),f[10].strftime("%H:%M"),f[11],f[12],f[13],f[14],f[15],f[16],f[17],f[18],f[19],f[20])
        #     # result = result.format(f[0],f[1],f[2],f[3],f[4],f[5],f[6],f[7],f[8],f[9],f[10],f[11],f[12],f[13],f[14],f[15],f[16],f[17],f[18],f[19],f[20],f[21])
        #     flight_list[result2] = f[0]
        #     result_str += result2 + '\n'


        ta  = print_table(flights)
        ui.codebox("Available Flights. Select one and click OK to Make a Booking", "FlightFinder", ta)
    else:
        ui.msgbox("No Flights Found From {} to {} on {}".format(src,dest,date), "Error")


    search_screen(user)





def bookings_screen(user):

    find_bookings = "SELECT tno, name, dep_date, paid_price " \
                        "FROM tickets NATURAL JOIN bookings " \
                        "WHERE LOWER(email)= LOWER('{}')".format(user._email)

    bookings = user._db.query(find_bookings)
    booking_list = {}

    if bookings:
        for b in bookings:
            b_info = "Ticket no. = {} \n Name = {} \n Date = {} \n Price = {}\n"\
                .format(b[0], b[1].strip(), b[2].strftime("%d-%b-%Y"), b[3])
            booking_list[b_info] = b[0]

        selected = ui.choicebox("Select a booking and click OK to see more details and options",
                     "Existing Bookings", booking_list.keys())

        if selected is None:
            main_screen(user)
        booking_detail_screen(user, booking_list.get(selected))
    else:
        ui.msgbox("This user has no bookings")
        main_screen(user)

def booking_detail_screen(user, tno):
    find_bookings = "SELECT tno, name, dep_date, paid_price, email, flightno, src, dst, fare, est_dur, seat " \
                        "FROM tickets NATURAL JOIN bookings NATURAL JOIN flight_fares NATURAL JOIN flights " \
                        "WHERE LOWER(email) = LOWER('{}') AND tno = '{}'".format(user._email, tno)
    bookings = user._db.query(find_bookings)
    booking_info = ""
    if bookings:
        b = bookings[0]
        booking_data = {"Ticket no.": b[0], "Name": b[1].strip(), "Date": b[2].strftime("%d-%b-%Y"), "Price": b[3],
                             "Email": b[4].strip(), "Flight no.":b[5], "Source": b[6], "Destination":b[7],
                             "Fare":b[8], "Estimated Duration":b[9], "Seat":b[10]}
        for key, value in booking_data.iteritems():
            booking_info += key + ": " + str(value) + "\n"
        choice = ui.buttonbox(booking_info, "Booking Details", ["Cancel Booking", "Back"],default_choice="Back", cancel_choice="Back")
        if choice == "Cancel Booking":
            user._db.execute("DELETE FROM bookings WHERE tno = '{}' AND flightno = '{}' AND to_char(dep_date,'DD/MM/YYYY') = '{}'"
                             .format(b[0], b[5], b[2].strftime("%d/%m/%Y")))
            ui.msgbox("Cancelled booking")
            bookings_screen(user)
        else:
            bookings_screen(user)



def make_booking_screen(user):
    ui.msgbox("Make booking")
    main_screen(user)

def r_dept_screen(user):
    ui.msgbox("Record Departure")
    main_screen(user)

def r_arr_screen(user):
    ui.msgbox("Record Arrival")
    main_screen(user)


def logout_screen(user):
    db = user._db
    if user.logout():
        splash_screen(db)
    else:
        main_screen(user)




def db_login_screen():
    db = DB()
    msg = "Enter Oracle Connection Information"
    title = "Connect to Oracle"
    fieldNames = ["Host", "Port", "SID", "Username", "Password"]
    fieldValues = ["localhost", "1525", "crs", "jutt", "ps3hammad"]
    errmsg = msg

    while 1:
        fieldValues = ui.multpasswordbox(errmsg, title, fieldNames, fieldValues)
        if fieldValues is None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg += '"%s" is a required field.\n\n' % fieldNames[i]

        if errmsg == "" and db.connect(fieldValues[0],fieldValues[1],fieldValues[2],fieldValues[3],fieldValues[4]):
            return db  # no problems found
    return None

def login_screen(db):
    credentials = formPrompt("Login to Flight Finder", "Login", ["Email", "Password"], 1)
    if credentials is None:
        splash_screen(db)

    user = User(credentials[0], credentials[1])

    if user.login(db):
        main_screen(user)
    else:
        ui.msgbox("Login Failed", "Error")
        login_screen(db)

def register_screen(db):
    credentials = formPrompt("Register for Flight Finder", "Register", ["Email", "Password"], 1)
    if credentials is None:
        splash_screen(db)

    user = User(credentials[0], credentials[1])

    if user.register(db):
        ui.msgbox("{} has been registered. Logging you in...".format(user._email), "Success")
        main_screen(user)
    else:
        ui.msgbox("Registration Failed", "Error")
        register_screen(db)

def splash_screen(db):

    while 1:
        choice = ui.indexbox("Welcome to Flight Finder", "Login/Register", ['Login', 'Register', 'Exit'])

        # Login
        if choice == 0:
            login_screen(db)
        # Register
        elif choice == 1:
            register_screen(db)
        # Exit
        else:
            db.close()
            sys.exit(0)


