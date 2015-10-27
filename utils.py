import datetime
from uiController import *


def execute_file(db, filename):

    with open(filename, "r") as datafile:
        data = ""
        for line in datafile:
            data += line.replace('\n', ' ')

        data = data.split(';')
    for cmd in data:
        db.execute(cmd)


def date_valid(date_str):
    try:
        datetime.datetime.strptime(date_str, '%d-%m-%Y')
        return True
    except ValueError:
        return False

def get_acode(db, query):

    ac_query = "SELECT acode, name, city FROM airports WHERE LOWER(acode) = LOWER('{0}') " \
               "OR LOWER(name) LIKE LOWER('%{0}%') OR LOWER(city) LIKE LOWER('%{0}%')".format(query)
    result = db.query(ac_query)

    if len(result) > 1:
        selected = ui.choicebox("Multiple airports matched for query: '{}'. Select one:".format(query), "FlightFinder",result)
        return selected[2:5]
    elif result:
        return result[0][0]
    else:
        return None