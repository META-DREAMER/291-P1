import cx_Oracle
from utils import *

class DB:
    def __init__(self):
        self._connection = None
        self._curs = None

    def connect(self, host, port, sid, username, pwd):
        conString = username + '/' + pwd + '@' + host + ':' + port + '/' + sid
        try:
            self._connection = cx_Oracle.connect(conString)
            self._curs = self._connection.cursor()
            return True  # no problems found
        except cx_Oracle.DatabaseError as exc:
            self._connection = None
            self._curs = None
            ui.msgbox(exc.args[0], "Error")
            return False

    def close(self):
        if self._connection is not None and self._curs is not None:
            self._curs.close()
            self._connection.close()
            self._connection = None
            self._curs = None

    def query(self, statement):
        if self._connection is not None and self._curs is not None:
            try:
                if self._curs.execute(statement):
                    return self._curs.fetchall()
            except cx_Oracle.DatabaseError as exc:
                ui.msgbox(exc.args[0], "Error")
                return None
            return []

    def execute(self, statement):
        if self._connection is not None:
            result = self.query(statement)
            self._connection.commit()
            return result


