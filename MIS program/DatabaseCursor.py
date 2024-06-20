import pyodbc
from DatabaseTable import DatabaseTable


class DatabaseCursor:
    def __init__(self, server, database, username, password):
        # 指定服务器、数据库、登录名和密码来连接数据库
        # 服务器选择参数，登录方式为SQL 身份验证，选择默认账号sa，密码需要重置
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        # 选择本设备的ODBC驱动器来连接
        self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database +
                                   ';ENCRYPT=yes;UID=' + username + ';PWD=' + password + ';TrustServerCertificate=yes')
        self.cursor = self.cnxn.cursor()
        self.connect = True  # 用于判断是否连接成功
        if not self.cursor:
            self.connect = False
            print('Connection Error')

    def insert(self, table_name, columns_number, new_records):
        # 向某个表的某些列插入一行或多行数据, columns_number为列名序号列表(如[1, 3]表示插入第1和3列)， new_records为元组列表，new_records中要插入的列都相同
        count = 0
        column_names = ''
        values = ''
        for index, column in enumerate(DatabaseTable[table_name]):
            if index == columns_number[count] - 1:  # 选择要插入的列
                if count == 0:  # 第一列
                    column_names += column
                    values += '?'
                else:
                    column_names += ', ' + column
                    values += ', ?'
                count += 1
                if count > len(columns_number) - 1:  # 选完了要插入的列
                    break
        # 此处count为插入的行数
        count = 0
        for index, record in enumerate(new_records):
            count += self.cursor.execute("INSERT INTO " + table_name + "(" + column_names + ")" + " VALUES" + "(" + values + ")", record).rowcount
        self.cursor.commit()  # 提交事务，保存
        print("The number of rows inserted: " + str(count))

    def delete(self, table_name, conditions):  # 删除某个表的指定记录, conditions是where语句要用的条件, conditions为str类型
        print("DELETE FROM " + table_name + " WHERE " + conditions)
        count = self.cursor.execute("DELETE FROM " + table_name + " WHERE " + conditions).rowcount
        self.cursor.commit()
        print("The number of rows deleted: " + str(count))

    def update(self, table_name, set_clause, conditions):
        print("UPDATE " + table_name + " SET " + set_clause + " WHERE " + conditions)
        count = self.cursor.execute("UPDATE " + table_name + " SET " + set_clause + " WHERE " + conditions).rowcount
        self.cursor.commit()
        print("The number of rows modified: " + str(count))

    def select(self, sql):  # table_names为from后跟的表名, 为str列表
        self.cursor.execute(sql)
        result = []
        for row in self.cursor.fetchall():
            result.append(tuple(row))
        return result  # 返回元组列表
