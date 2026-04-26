from sqlite3 import Connection

class CursorSingleton():
    _instance = None

    @staticmethod
    def get_instance(conn: Connection):
        if CursorSingleton._instance is None:
            CursorSingleton._instance = conn.cursor()
        return CursorSingleton._instance