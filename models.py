import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="1bC@111111",
    database="demo01"
)

print("MySQL 連線成功！")

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
        conn.rollback()
        # 關閉連接
        conn.close()
        return type(err_massage), err_massage

# username = "張三"

# code = "INSERT INTO `login_user` (`username`, `password`) VALUES ('%s', '%s')" %(username, pwd)
# print(con_mySQL(code))

username = "張三"
code = "select * from login_user"
cursor_ans = con_mySQL(code)
print(cursor_ans.fetchall())



# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# import mysql.connector

# db = SQLAlchemy()
# # 設定 MySQL 連線參數
# db_config = {
#     "host": "localhost",
#     "user": "root",
#     "password": "1bC@111111",
#     "database": "demo01"
# }

# # 建立連線函式
# def get_db_connection():
#     """建立並回傳 MySQL 資料庫連線"""
#     conn = mysql.connector.connect(**db_config)
#     return conn

# # 定義資料庫操作函式
# def insert_user(username, password):
#     """插入新使用者"""
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
#     cursor.execute(sql, (username, password))
    
#     conn.commit()
#     cursor.close()
#     conn.close()

# def get_user(username):
#     """查詢使用者資料"""
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)  # 讓回傳結果為字典格式
    
#     sql = "SELECT * FROM users WHERE username = %s"
#     cursor.execute(sql, (username,))
    
#     result = cursor.fetchone()
    
#     cursor.close()
#     conn.close()
    
#     return result

# def set_password(self, password):
#     self.password = generate_password_hash(password)

# def check_password(self, password):
#     return check_password_hash(self.password, password)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)
