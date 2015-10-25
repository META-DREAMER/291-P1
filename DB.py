import cx_Oracle
import gui.easygui as ui

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

    def execute(self, query):
        if self._connection is not None and self._curs is not None:
            try:
                if self._curs.execute(query):
                    return self._curs.fetchall()
                return []
            except cx_Oracle.DatabaseError as exc:
                ui.msgbox(exc.args[0], "Error")
                return False

    def commit(self, query):
        if self._connection is not None:
            self.execute(query)
            self._connection.commit()

    def __del__(self):
        self.close()