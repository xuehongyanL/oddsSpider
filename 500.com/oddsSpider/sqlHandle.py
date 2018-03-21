class sql():
    def __init__(self):
        pass

    def execute(self, t):
        self.c.execute(t)

    def fetch(self, n=0):
        if n:
            return self.c.fetchmany(n)
        return self.c.fetchall()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def sqlGet(self, table, select='*', where="", orderby=""):
        t = '''SELECT {0} FROM {1}'''.format(select, table)
        if where:
            t += '\nWHERE {0}'.format(where)
        if orderby:
            t += '\nORDER BY {0}'.format(orderby)
        t += ';'
        self.c.execute(t)
        return self.c.fetchall()


class sqlite(sql):
    def __init__(self, file):
        import sqlite3
        self.conn = sqlite3.connect(file)
        self.c = self.conn.cursor()


class mysql(sql):
    def __init__(self, login):
        import pymysql
        self.conn = pymysql.connect(**login)
        self.c = self.conn.cursor()


class sqlServer(sql):
    def __init__(self, login):
        import pymssql
        self.conn = pymssql.connect(**login)
        self.c = self.conn.cursor()
