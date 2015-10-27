from uiController import *

class User:
    def __init__(self, email, pwd):
        self._email = email
        self._pwd = pwd
        self._db = None
        self._is_agent = False

    def login(self, db):
        if db.query("SELECT u.email FROM users u WHERE LOWER(u.email) = LOWER('{}') AND u.pass = '{}'".format(self._email.lower(), self._pwd)):
            self._db = db
            if self._db.query("SELECT * FROM airline_agents a WHERE LOWER(a.email) = LOWER('{}')".format(self._email.lower())):
                self._is_agent = True
            return True
        else:
            return False

    def register(self, db):
        if db.query("SELECT u.email FROM users u WHERE LOWER(u.email) = LOWER('{}')".format(self._email.lower())) == []:
            if db.execute("INSERT INTO users (email, pass) VALUES ('{}', '{}')".format(self._email, self._pwd)) is not None:
                return self.login(db)
        else:
            ui.msgbox("User Already Exists.", "Error")

        return False

    def logout(self):
        if self._db is not None:
            if self._db.execute("UPDATE users SET last_login = sysdate WHERE LOWER(email) = LOWER('{}')".format(self._email)) is not None:
                self._db = None
                return True
            return False
        else:
            ui.msgbox("User already logged out.", "Info")
            return True
