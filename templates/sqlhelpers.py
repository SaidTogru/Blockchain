from app import mysql, session


class InvalidTransactionException(Exception):
    pass


class InsufficientFundsException(Exception):
    pass


class Table:
    def __init__(self, table_name, *args):
        self.table = table_name
        self.columns = "(%s)" % ",".join(args)
        self.columnsList = args

        if isnewtable(table_name):
            create_data = ""
            cur = mysql.connection.cursor()
            cur.execute("CREATE TABLE %s%s" % (self.table, self.columns))
            cur.close()

    def getall(self):
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s" % self.table)
        data = cur.fetchall()
        return data

    def getone(self, search, value):
        data = {}
        cur = mysql.connection.cursor()
        result = cur.execute(
            'SELECT * FROM %s WHERE %s = "%s"' % (self.table, search, value)
        )
        if result > 0:
            data = cur.fetchone()
            cur.close()
            return data

    def deleteone(self, search, value):
        cur = mysql.connection.cursor()
        cur.execute('DELETE * FROM %s WHERE %s = "%s"' % (self.table, search, value))
        mysql.connection.commit()
        cur.close()

    def drop(self):
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE %s" % self.table)
        cur.close()

    def insert(self, *args):
        data = ""
        for arg in args:
            data += '"%s",' % (arg)

        cur = mysql.connection.cursor()
        cur.execute(
            "INSER INTO %s%s VALUES(%s)"
            % (self.table, self.columns, data[: len(data) - 1])
        )
        mysql.connection.commit()
        cur.close()


def sql_raw(execution):
    cur = mysql.connection.cursor()
    cur.execute(execution)
    mysql.connection.commit()
    cur.close()


def isnewtable(tableName):
    cur = mysql.connection.cursor()

    try:
        result = cur.execute("SELECT * FROM %s" % tableName)
        cur.close()
    except:
        return True
    else:
        return False
