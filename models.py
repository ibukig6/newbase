import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="1bC@111111",
    database="demo01"
)

def con_mySQL(sql_code):
    try:
        conn.ping(reconnect=True)
        print(sql_code)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql_code)

        conn.commit()

        conn.close()
        return cursor
    except pymysql.MySQLError as err_massage:

        conn.close()
        return type(err_massage), err_massage

# username = "張三"

# code = "INSERT INTO `login_user` (`username`, `password`) VALUES ('%s', '%s')" %(username, pwd)
# print(con_mySQL(code))

username = "張三"
code = "select * from login_user"
cursor_ans = con_mySQL(code)
print(cursor_ans.fetchall())
