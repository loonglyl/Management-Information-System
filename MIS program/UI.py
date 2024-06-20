import tkinter as tk
import time
from tkinter import messagebox, ttk
from DatabaseCursor import DatabaseCursor
from DatabaseTable import DatabaseTable, DatabaseColumnTypes
from PIL import Image, ImageTk


def mis_window_of_student():  # 学生看到的窗口
    mise.destroy()
    mis = tk.Tk()  # 创建第二个窗口
    wt, ht = 720, 480
    centerx, centery = int((screen_size[0] - width) / 2), int((screen_size[1] - height) / 2) - 200  # 计算左上角坐标
    mis.title("Management Information System")
    mis.geometry('%dx%d+%d+%d' % (wt, ht, centerx, centery))
    mis.update()
    timestamp1 = [time.time()]
    timestamp2 = [time.time()]
    mis_saved_width = [wt]
    table_width = [450, 450]  # [0]为旧值，[1]为新值
    current_table = []

    def scale(event):
        table_width[0] = table_width[1]  # 记录旧值
        table_width[1] += mis.winfo_width() - mis_saved_width[0]  # 重新设置表的宽度
        mis_saved_width[0] = mis.winfo_width()
        content_label.config(width=int(table_width[0]//9))
        timestamp2[0] = time.time()
        # 只有表宽度变化的时候才调用choose_table
        if table_width[0] - table_width[1] != 0 and \
                timestamp2[0] - timestamp1[0] >= 0.5:  # treeview更新的时候scale也会被调用，导致查询结果被覆盖
            choose_table()
        timestamp1[0] = time.time()

    def show_search_result(result):
        idx = choice.get()
        column_list = DatabaseTable[list(DatabaseTable.keys())[idx]]
        wd = table_width[1] // len(column_list)  # 平均列宽
        table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
        for column in column_list:
            table.heading(column, text=column)
            table.column(column, width=wd, minwidth=wd, anchor="center")
        for i, record in enumerate(result):
            table.insert('', index=i, values=record)
        current_table[0].destroy()  # 删除原来的表
        current_table[0] = table  # 记录当前表
        table.grid(row=1, column=0, sticky='w')

    def choose_table():
        idx = choice.get()
        if idx == 0:  # Student
            search_student.grid(row=1, column=0)
            search_score.grid_forget()
            search_course.grid_forget()
            search_teaches.grid_forget()
            search_average.grid_forget()
        elif idx == 1:  # Course
            search_student.grid_forget()
            search_score.grid_forget()
            search_course.grid(row=1, column=0)
            search_teaches.grid_forget()
            search_average.grid_forget()
        elif idx == 2:  # Teacher
            search_student.grid_forget()
            search_score.grid_forget()
            search_course.grid_forget()
            search_teaches.grid_forget()
            search_average.grid_forget()
        elif idx == 3:  # Teaches
            search_student.grid_forget()
            search_score.grid_forget()
            search_course.grid_forget()
            search_teaches.grid(row=1, column=0)
            search_average.grid_forget()
        elif idx == 4:  # Course choosing
            search_student.grid_forget()
            search_score.grid(row=1, column=0)
            search_course.grid_forget()
            search_teaches.grid_forget()
            search_average.grid(row=2, column=0)
        if idx == 1 or 3:
            column_list = DatabaseTable[list(DatabaseTable.keys())[idx]]
            wd = table_width[1] // len(column_list)  # 平均列宽
            table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
            for column in column_list:
                table.heading(column, text=column)
                table.column(column, width=wd, minwidth=wd, anchor="center")
            result = cursor.select('SELECT * FROM ' + list(DatabaseTable.keys())[idx])  # 查询表
            for i, record in enumerate(result):
                table.insert('', index=i, values=record)
            if len(current_table) == 0:  # 初始化
                current_table.append(table)
            else:
                current_table[0].destroy()  # 删除原来的表
                current_table[0] = table  # 记录当前表
            table.grid(row=1, column=0, sticky='w')
        else:
            column_list = DatabaseTable[list(DatabaseTable.keys())[idx]]
            wd = table_width[1] // len(column_list)  # 平均列宽
            table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
            for column in column_list:
                table.heading(column, text=column)
                table.column(column, width=wd, minwidth=wd, anchor="center")
            if len(current_table) == 0:  # 初始化
                current_table.append(table)
            else:
                current_table[0].destroy()  # 删除原来的表
                current_table[0] = table  # 记录当前表
            table.grid(row=1, column=0, sticky='w')

    def search_score():  # 用学生ID或名字和课程ID或名称查选课信息和分数
        def confirm():
            attribute1 = combobox_list[0].get()
            attribute2 = combobox_list[1].get()
            if len(attribute1) == 0 and len(attribute2) == 0:
                sql = f"SELECT S.Name, C2.Name, T.Name, C1.Score " \
                      f"FROM Course_Choosing as C1, Student as S, Course as C2, Teacher as T" \
                      f" WHERE C1.Student_ID=S.ID and C1.Course_ID=C2.ID and C1.Teacher_ID=T.ID"
                result = cursor.select(sql)
                column_list = ['Student Name', 'Course Name', 'Teacher Name', 'Score']
                wd = table_width[1] // len(column_list)  # 平均列宽
                table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
                for column in column_list:
                    table.heading(column, text=column)
                    table.column(column, width=wd, minwidth=wd, anchor="center")
                for i, record in enumerate(result):
                    table.insert('', index=i, values=record)
                current_table[0].destroy()  # 删除原来的表
                current_table[0] = table  # 记录当前表
                table.grid(row=1, column=0, sticky='w')
                return 0
            record = [value_list[i].get() for i in range(len(value_list))]  # 获取where条件，做字符串and连接处理和加引号处理
            types = DatabaseColumnTypes[list(DatabaseTable.keys())[idx]]  # 获得当前表的每一列的类型，进行类型检查，加引号
            condition = ''
            for i in range(len(record)):  # where语句条件
                if len(record[i]) != 0:  # 输入不为空
                    if i == 0:
                        a = 'S.'
                    else:
                        a = 'C2.'
                    if len(condition) == 0:
                        condition += a + combobox_list[i].get() + '='
                        if types[i] == 'int':
                            condition += record[i]
                        else:
                            condition += "'" + record[i] + "'"  # 对string类型加引号
                    else:
                        condition += f' and {a}' + combobox_list[i].get() + '='
                        if types[i] == 'int':
                            condition += record[i]
                        else:
                            condition += "'" + record[i] + "'"  # 对string类型加引号
            if len(condition) != 0:
                sql = f"SELECT S.Name, C2.Name, T.Name, C1.Score " \
                      f"FROM Course_Choosing as C1, Student as S, Course as C2, Teacher as T" \
                      f" WHERE {condition} and " \
                      f"C1.Student_ID=S.ID and C1.Course_ID=C2.ID and C1.Teacher_ID=T.ID"
            else:
                sql = f"SELECT S.Name, C2.Name, T.Name, C1.Score " \
                      f"FROM Course_Choosing as C1, Student as S, Course as C2, Teacher as T" \
                      f" WHERE C1.Student_ID=S.ID and C1.Course_ID=C2.ID and C1.Teacher_ID=T.ID"
            result = cursor.select(sql)
            column_list = ['Student Name', 'Course Name', 'Teacher Name', 'Score']
            wd = table_width[1] // len(column_list)  # 平均列宽
            table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
            for column in column_list:
                table.heading(column, text=column)
                table.column(column, width=wd, minwidth=wd, anchor="center")
            for i, record in enumerate(result):
                table.insert('', index=i, values=record)
            current_table[0].destroy()  # 删除原来的表
            current_table[0] = table  # 记录当前表
            table.grid(row=1, column=0, sticky='w')

        def cancel():
            child_window.destroy()

        idx = choice.get()
        column_list = ['Student Information', 'Course Information']
        child_window = tk.Toplevel(mis)  # 创建一个子窗口
        child_window.title('Search scores from current table ' + list(DatabaseTable.keys())[idx])
        child_window.geometry('+%d+%d' % (int((screen_size[0]-child_window.winfo_reqwidth())/2) - 100,
                                          (int((screen_size[1]-child_window.winfo_reqheight())/2))))
        main_frame = tk.Frame(child_window, bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True)
        value_list = [tk.StringVar() for i in range(len(column_list))]
        combobox_list = []
        for i, column in enumerate(column_list):  # 放置条件输入框，conditions
            tk.Label(main_frame, text=column, font=("Times New Roman", 12), width=20).grid(row=0, column=i, pady=10)
            tk.Entry(main_frame, textvariable=value_list[i], width=20).grid(row=2, column=i, pady=10)
            combo = ttk.Combobox(main_frame, values=('ID', 'Name'), state='readonly',
                                 font=("Times New Roman", 12), cursor='arrow', width=5)
            combobox_list.append(combo)
            combo.grid(row=1, column=i)
        # 添加确定和取消按钮
        b_frame = tk.Frame(child_window, bd=2, relief='groove')
        b_frame.pack(side='bottom', fill='both', expand=True)
        tk.Button(b_frame, text='Confirm', width=10, command=confirm).pack(side='left')
        tk.Button(b_frame, text='Cancel', width=10, command=cancel).pack(side='right')

    def search_course():  # 用课程ID或名称查询课程信息，表Course
        def confirm():
            record = [value_list[i].get() for i in range(len(value_list))]  # 获取where条件，做字符串and连接处理和加引号处理
            names = DatabaseTable[list(DatabaseTable.keys())[idx]]  # 获取当前表的每一列的名字
            types = DatabaseColumnTypes[list(DatabaseTable.keys())[idx]]  # 获得当前表的每一列的类型，进行类型检查，加引号
            condition = ''
            for i in range(len(record)):  # where语句条件
                if len(record[i]) != 0:  # 输入不为空
                    if len(condition) == 0:  # 第一个条件
                        condition += list(DatabaseTable.keys())[idx] + '.' + names[i] + '='
                        if types[i] == 'int':
                            condition += record[i]
                        else:
                            condition += "'" + record[i] + "'"  # 对string类型加双引号
                    else:
                        condition += ' and ' + list(DatabaseTable.keys())[idx] + '.' + names[i] + '='
                        if types[i] == 'int':
                            condition += record[i]
                        else:
                            condition += "'" + record[i] + "'"  # 对string类型加双引号
            if len(condition) != 0:
                result = cursor.select("Select * FROM " + list(DatabaseTable.keys())[idx] + " WHERE " + condition)
                show_search_result(result)  # 展示查询结果
            else:
                choose_table()  # 默认显示所有课程的信息

        def cancel():
            child_window.destroy()

        idx = choice.get()
        column_list = DatabaseTable[list(DatabaseTable.keys())[idx]][:2]  # 前两项ID、Name
        child_window = tk.Toplevel(mis)  # 创建一个子窗口
        child_window.title('Search courses from current table ' + list(DatabaseTable.keys())[idx])
        child_window.geometry('+%d+%d' % (int((screen_size[0] - child_window.winfo_reqwidth()) / 2) - 100,
                                          (int((screen_size[1] - child_window.winfo_reqheight()) / 2))))
        main_frame = tk.Frame(child_window, bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True)
        value_list = [tk.StringVar() for i in range(len(column_list))]
        for i, column in enumerate(column_list):  # 放置条件输入框，conditions
            tk.Label(main_frame, text=column, font=("Times New Roman", 12), width=20).grid(row=0, column=i, pady=10)
            tk.Entry(main_frame, textvariable=value_list[i], width=20).grid(row=1, column=i, pady=10)
        # 添加确定和取消按钮
        b_frame = tk.Frame(child_window, bd=2, relief='groove')
        b_frame.pack(side='bottom', fill='both', expand=True)
        tk.Button(b_frame, text='Confirm', width=10, command=confirm).pack(side='left')
        tk.Button(b_frame, text='Cancel', width=10, command=cancel).pack(side='right')

    def search_teaches():  # 用老师ID或名字查询老师教的课，表Teaches
        def confirm():
            id = value_list[0].get()
            name = value_list[1].get()
            record = [(id,)]
            if len(id) > 0 and len(name) > 0:  # 既有ID又有名称输入
                record = cursor.select(f"SELECT ID FROM Teacher WHERE Name='{name}'")  # 用名字查该老师的ID号
                if id != record[0][0]:
                    messagebox.showwarning(title="Inconsistent Input", message="Please check that ID"
                                                                               " and Name is correct.")
                    return 0  # 不兼容的输入，直接结束
            # 这里之后只有兼容的输入，没有条件，只有ID或只有名称，或者兼容的ID和名称
            elif len(id) == 0 and len(name) > 0:  # 只有名称的输入
                record = cursor.select(f"SELECT ID FROM Teacher WHERE Name='{name}'")  # 用名字查该老师的ID号
            condition = 'T1.Teacher_ID=' + record[0][0]
            if len(condition) > 14:
                sql = "Select T2.Name, C.Name FROM Teaches as T1, Teacher as T2, Course as C " \
                      "WHERE " + condition + " and T1.Teacher_ID=T2.ID and T1.Course_ID=C.ID"
            else:
                sql = "Select T2.Name, C.Name FROM Teaches as T1, Teacher as T2, Course as C " \
                      "WHERE T1.Teacher_ID=T2.ID and T1.Course_ID=C.ID"
            result = cursor.select(sql)
            column_list = ['Teacher Name', 'Course Name']
            wd = table_width[1] // len(column_list)  # 平均列宽
            table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
            for column in column_list:
                table.heading(column, text=column)
                table.column(column, width=wd, minwidth=wd, anchor="center")
            for i, record in enumerate(result):
                table.insert('', index=i, values=record)
            current_table[0].destroy()  # 删除原来的表
            current_table[0] = table  # 记录当前表
            table.grid(row=1, column=0, sticky='w')

        def cancel():
            child_window.destroy()

        idx = choice.get()
        column_list = ['Teacher ID', 'Teacher Name']
        child_window = tk.Toplevel(mis)  # 创建一个子窗口
        child_window.title('Search courses from current table ' + list(DatabaseTable.keys())[idx])
        child_window.geometry('+%d+%d' % (int((screen_size[0] - child_window.winfo_reqwidth()) / 2) - 100,
                                          (int((screen_size[1] - child_window.winfo_reqheight()) / 2))))
        main_frame = tk.Frame(child_window, bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True)
        value_list = [tk.StringVar() for i in range(len(column_list))]
        for i, column in enumerate(column_list):  # 放置条件输入框，conditions
            tk.Label(main_frame, text=column, font=("Times New Roman", 12), width=20).grid(row=0, column=i, pady=10)
            tk.Entry(main_frame, textvariable=value_list[i], width=20).grid(row=1, column=i, pady=10)
        # 添加确定和取消按钮
        b_frame = tk.Frame(child_window, bd=2, relief='groove')
        b_frame.pack(side='bottom', fill='both', expand=True)
        tk.Button(b_frame, text='Confirm', width=10, command=confirm).pack(side='left')
        tk.Button(b_frame, text='Cancel', width=10, command=cancel).pack(side='right')

    def search_average():  # 学生用自己的ID或名字查自己的平均分
        def confirm():
            if len(combo.get()) == 0:
                messagebox.showwarning(title="No Selection", message="Please select an attribute to search.")
            elif len(value_list[0].get()) == 0:
                messagebox.showwarning(title="Empty Input Warning", message="No valid input, please check input.")
            else:
                sql = "select S.Name, AVG(Score) as Average_Score " \
                      "from Course_Choosing as C, Student as S " \
                      "where C.Student_ID=S.ID and S." + combo.get() + "='" + value_list[0].get() + "'" \
                      " group by S.Name"
                column_list = ['Student Name', 'Average Score']
                wd = table_width[1] // len(column_list)  # 平均列宽
                table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
                for column in column_list:
                    table.heading(column, text=column)
                    table.column(column, width=wd, minwidth=wd, anchor="center")
                result = cursor.select(sql)
                for i, record in enumerate(result):
                    table.insert('', index=i, values=record)
                current_table[0].destroy()  # 删除原来的表
                current_table[0] = table  # 记录当前表
                table.grid(row=1, column=0, sticky='w')

        def cancel():
            child_window.destroy()

        column_list = ['Student Information']
        child_window = tk.Toplevel(mis)  # 创建一个子窗口
        child_window.title('Search average score of a student')
        child_window.geometry('+%d+%d' % (int((screen_size[0] - child_window.winfo_reqwidth()) / 2) - 100,
                                          (int((screen_size[1] - child_window.winfo_reqheight()) / 2))))
        main_frame = tk.Frame(child_window, bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True)
        value_list = [tk.StringVar() for i in range(len(column_list))]

        tk.Label(main_frame, text='Student Information', font=("Times New Roman", 12), width=20).grid(row=0, column=0, pady=10)
        tk.Entry(main_frame, textvariable=value_list[0], width=20).grid(row=2, column=0, pady=10)
        combo = ttk.Combobox(main_frame, values=('ID', 'Name'), state='readonly',
                             font=("Times New Roman", 12), cursor='arrow', width=5)
        combo.grid(row=1, column=0)
        # 添加确定和取消按钮
        b_frame = tk.Frame(child_window, bd=2, relief='groove')
        b_frame.pack(side='bottom', fill='both', expand=True)
        tk.Button(b_frame, text='Confirm', width=10, command=confirm).pack(side='left')
        tk.Button(b_frame, text='Cancel', width=10, command=cancel).pack(side='right')

    # 基础界面
    table_list_frame = tk.Frame(mis, bd=2, relief='groove')
    table_list_frame.pack(side='left', fill='y', expand=True)
    choice = tk.IntVar()
    tk.Label(table_list_frame, text="Tables", font=("Times New Roman", 12), width=15,
             background='lightskyblue').grid(row=0, column=0)
    for index, key in enumerate(DatabaseTable.keys()):  # 为所有表创建选择键
        if key != 'Account' and key != 'Teacher':
            tk.Radiobutton(table_list_frame, highlightcolor='blue', text=key,
                           variable=choice, value=index, anchor='w', indicatoron=False,
                           font=("Times New Roman", 12), width=15, command=choose_table).grid(row=index + 1, column=0)
    # 表内容子窗口
    content_frame = tk.Frame(mis, bd=2, relief='groove')
    content_frame.pack(side='left', fill='both', expand=True)
    content_label = tk.Label(content_frame, text="Content", font=("Times New Roman", 12), width=50,
                             background='lightskyblue')
    content_label.grid(row=0, column=0, sticky='w')
    # 功能键子窗口
    button_frame = tk.Frame(mis, bd=2, relief='groove')
    button_frame.pack(side='left', fill='y', expand=True)
    tk.Label(button_frame, text="Functions", font=("Times New Roman", 12), background='lightskyblue', width=12).grid(
        row=0, column=0)
    # 查询功能键
    search_student = tk.Button(button_frame, text="Search student", width=12, command=search_course)
    search_score = tk.Button(button_frame, text="Search course\nand score", width=12, command=search_score)
    search_teaches = tk.Button(button_frame, text="Search teaches", width=12, command=search_teaches)
    search_course = tk.Button(button_frame, text="Search course", width=12, command=search_course)
    search_average = tk.Button(button_frame, text="Average\nscore", width=12, command=search_average)
    # 初始化
    choose_table()  # 获得当前表
    mis.bind('<Configure>', scale)  # 将屏幕大小变化事件和控件大小变化事件绑定在一起
    mis.mainloop()


# ---------------------------------------------------------------------------------------------------------------


def mis_window_of_teacher():  # 老师看到的窗口
    mise.destroy()
    mis = tk.Tk()  # 创建第二个窗口
    wt, ht = 720, 480
    centerx, centery = int((screen_size[0] - width) / 2), int((screen_size[1] - height) / 2) - 200  # 计算左上角坐标
    mis.title("Management Information System")
    mis.geometry('%dx%d+%d+%d' % (wt, ht, centerx, centery))
    mis.update()
    timestamp1 = [time.time()]
    timestamp2 = [time.time()]
    mis_saved_width = [wt]
    table_width = [450, 450]  # [0]为旧值，[1]为新值
    current_table = []

    def scale(event):
        table_width[0] = table_width[1]  # 记录旧值
        table_width[1] += mis.winfo_width() - mis_saved_width[0]  # 重新设置表的宽度
        mis_saved_width[0] = mis.winfo_width()
        content_label.config(width=int(table_width[0]//9))
        timestamp2[0] = time.time()
        # 只有表宽度变化的时候才调用choose_table
        if table_width[0] - table_width[1] != 0 and \
                timestamp2[0] - timestamp1[0] >= 0.5:  # treeview更新的时候scale也会被调用，导致查询结果被覆盖
            choose_table()
        timestamp1[0] = time.time()

    def show_search_result(result):
        idx = choice.get()
        column_list = DatabaseTable[list(DatabaseTable.keys())[idx]]
        wd = table_width[1] // len(column_list)  # 平均列宽
        table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
        for column in column_list:
            table.heading(column, text=column)
            table.column(column, width=wd, minwidth=wd, anchor="center")
        for i, record in enumerate(result):
            table.insert('', index=i, values=record)
        current_table[0].destroy()  # 删除原来的表
        current_table[0] = table  # 记录当前表
        table.grid(row=1, column=0, sticky='w')

    def choose_table():
        idx = choice.get()
        if idx == 1:  # Course
            update.grid_forget()
            search_course.grid(row=1, column=0)
            search_teacher.grid_forget()
            search_teaches.grid_forget()
            search_course_choosing.grid_forget()
            search_average3.grid_forget()
        elif idx == 2:  # Teacher
            update.grid_forget()
            search_course.grid_forget()
            search_teacher.grid(row=1, column=0)
            search_teaches.grid_forget()
            search_course_choosing.grid_forget()
            search_average3.grid_forget()
        elif idx == 3:  # Teaches
            update.grid_forget()
            search_course.grid_forget()
            search_teacher.grid_forget()
            search_teaches.grid(row=1, column=0)
            search_course_choosing.grid_forget()
            search_average3.grid_forget()
        elif idx == 4:  # Course choosing
            update.grid(row=1, column=0)
            search_course.grid_forget()
            search_teacher.grid_forget()
            search_teaches.grid_forget()
            search_course_choosing.grid(row=2, column=0)
            search_average3.grid(row=3, column=0)
        if idx == 1 or idx == 3:  # Course, Teaches
            column_list = DatabaseTable[list(DatabaseTable.keys())[idx]]
            wd = table_width[1] // len(column_list)  # 平均列宽
            table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
            for column in column_list:
                table.heading(column, text=column)
                table.column(column, width=wd, minwidth=wd, anchor="center")
            result = cursor.select('SELECT * FROM ' + list(DatabaseTable.keys())[idx])  # 查询表
            for i, record in enumerate(result):
                table.insert('', index=i, values=record)
            if len(current_table) == 0:  # 初始化
                current_table.append(table)
            else:
                current_table[0].destroy()  # 删除原来的表
                current_table[0] = table  # 记录当前表
            table.grid(row=1, column=0, sticky='w')
        else:
            column_list = DatabaseTable[list(DatabaseTable.keys())[idx]]
            wd = table_width[1] // len(column_list)  # 平均列宽
            table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
            for column in column_list:
                table.heading(column, text=column)
                table.column(column, width=wd, minwidth=wd, anchor="center")
            if len(current_table) == 0:  # 初始化
                current_table.append(table)
            else:
                current_table[0].destroy()  # 删除原来的表
                current_table[0] = table  # 记录当前表
            table.grid(row=1, column=0, sticky='w')

    def update():  # 修改功能界面
        def confirm():
            # 获取where条件，做字符串and连接处理和加引号处理
            record = [condition_value_list[i].get() for i in range(len(condition_value_list))]
            names = DatabaseTable[list(DatabaseTable.keys())[idx]]  # 获取当前表的每一列的名字
            types = DatabaseColumnTypes[list(DatabaseTable.keys())[idx]]  # 获得当前表的每一列的类型，进行类型检查，加引号
            condition = ''
            for i in range(len(record)):  # where语句条件
                if len(record[i]) != 0:  # 输入不为空
                    if len(condition) == 0:
                        condition += list(DatabaseTable.keys())[idx] + '.' + names[i] + combobox_list[i].get()
                        if types[i] == 'int':
                            condition += record[i]
                        else:
                            condition += "'" + record[i] + "'"  # 对string类型加双引号
                    else:
                        condition += ' and ' + list(DatabaseTable.keys())[idx] + '.' + names[i] + combobox_list[i].get()
                        if types[i] == 'int':
                            condition += record[i]
                        else:
                            condition += "'" + record[i] + "'"  # 对string类型加双引号
            # 获取修改值，并做加逗号分隔处理
            new_record = [new_value_list[i].get() for i in range(len(new_value_list))]
            set_clause = ''
            for i in range(len(new_record)):  # where语句条件
                if len(new_record[i]) != 0:  # 输入不为空
                    if len(set_clause) == 0:
                        set_clause += list(DatabaseTable.keys())[idx] + '.' + names[i] + '='
                        if types[i] == 'int':
                            set_clause += new_record[i]
                        else:
                            set_clause += "'" + new_record[i] + "'"  # 对string类型加双引号
                    else:
                        set_clause += ', ' + list(DatabaseTable.keys())[idx] + '.' + names[i] + '='  # 逗号分隔
                        if types[i] == 'int':
                            set_clause += new_record[i]
                        else:
                            set_clause += "'" + new_record[i] + "'"  # 对string类型加双引号
            if len(condition) != 0 and len(set_clause) != 0:  # 两个都不为空才能修改
                cursor.update(list(DatabaseTable.keys())[idx], set_clause, condition)
                choose_table()  # 展示结果
            else:
                messagebox.showwarning(title="Empty Input or Condition Warning",
                                       message="No valid input or condition, please check input or condition.")

        def cancel():
            child_window.destroy()

        idx = choice.get()
        column_list = DatabaseTable[list(DatabaseTable.keys())[idx]]  # 当前表列名
        child_window = tk.Toplevel(mis)  # 创建一个子窗口
        child_window.title('Update records in the current table ' + list(DatabaseTable.keys())[idx])
        child_window.geometry('+%d+%d' % (int((screen_size[0] - child_window.winfo_reqwidth()) / 2) - 100,
                                          (int((screen_size[1] - child_window.winfo_reqheight()) / 2))))
        main_frame = tk.Frame(child_window, bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True)
        new_value_list = [tk.StringVar() for i in range(len(column_list))]  # 修改值的value列表
        condition_value_list = [tk.StringVar() for i in range(len(column_list))]  # 条件框的value列表
        combobox_list = []
        tk.Label(main_frame, text='New value:', font=("Times New Roman", 12), width=10).grid(row=1, column=0, pady=10)
        tk.Label(main_frame, text='Conditions:', font=("Times New Roman", 12), width=10).grid(row=3, column=0, pady=10)
        for i, column in enumerate(column_list):  # 放置条件输入框，conditions
            tk.Label(main_frame, text=column, font=("Times New Roman", 12), width=20).grid(row=0, column=i + 1, pady=10)
            if i == 4:  # Score
                tk.Entry(main_frame, textvariable=new_value_list[i], width=20).grid(row=1, column=i + 1, pady=10)  # 修改值输入框
            else:
                tk.Label(main_frame, font=("Times New Roman", 12), width=20).grid(row=1, column=i + 1, pady=10)
            tk.Entry(main_frame, textvariable=condition_value_list[i], width=20).grid(row=3, column=i + 1,
                                                                                      pady=10)  # 条件值输入框
            combo = ttk.Combobox(main_frame, values=('=', '<', '>', '>=', '<='), state='readonly',
                                 font=("Times New Roman", 12), cursor='arrow', width=5)
            combobox_list.append(combo)
            combo.grid(row=2, column=i + 1)

        # 添加确定和取消按钮
        b_frame = tk.Frame(child_window, bd=2, relief='groove')
        b_frame.pack(side='bottom', fill='both', expand=True)
        tk.Button(b_frame, text='Confirm', width=10, command=confirm).pack(side='left')
        tk.Button(b_frame, text='Cancel', width=10, command=cancel).pack(side='right')

    def search_course():  # 用课程ID或名称查询课程信息，表Course
        def confirm():
            record = [value_list[i].get() for i in range(len(value_list))]  # 获取where条件，做字符串and连接处理和加引号处理
            names = DatabaseTable[list(DatabaseTable.keys())[idx]]  # 获取当前表的每一列的名字
            types = DatabaseColumnTypes[list(DatabaseTable.keys())[idx]]  # 获得当前表的每一列的类型，进行类型检查，加引号
            condition = ''
            for i in range(len(record)):  # where语句条件
                if len(record[i]) != 0:  # 输入不为空
                    if len(condition) == 0:  # 第一个条件
                        condition += list(DatabaseTable.keys())[idx] + '.' + names[i] + '='
                        if types[i] == 'int':
                            condition += record[i]
                        else:
                            condition += "'" + record[i] + "'"  # 对string类型加双引号
                    else:
                        condition += ' and ' + list(DatabaseTable.keys())[idx] + '.' + names[i] + '='
                        if types[i] == 'int':
                            condition += record[i]
                        else:
                            condition += "'" + record[i] + "'"  # 对string类型加双引号
            if len(condition) != 0:
                result = cursor.select("Select * FROM " + list(DatabaseTable.keys())[idx] + " WHERE " + condition)
                show_search_result(result)  # 展示查询结果
            else:
                choose_table()  # 默认显示所有课程的信息

        def cancel():
            child_window.destroy()

        idx = choice.get()
        column_list = DatabaseTable[list(DatabaseTable.keys())[idx]][:2]  # 前两项ID、Name
        child_window = tk.Toplevel(mis)  # 创建一个子窗口
        child_window.title('Search courses from current table ' + list(DatabaseTable.keys())[idx])
        child_window.geometry('+%d+%d' % (int((screen_size[0] - child_window.winfo_reqwidth()) / 2) - 100,
                                          (int((screen_size[1] - child_window.winfo_reqheight()) / 2))))
        main_frame = tk.Frame(child_window, bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True)
        value_list = [tk.StringVar() for i in range(len(column_list))]
        for i, column in enumerate(column_list):  # 放置条件输入框，conditions
            tk.Label(main_frame, text=column, font=("Times New Roman", 12), width=20).grid(row=0, column=i, pady=10)
            tk.Entry(main_frame, textvariable=value_list[i], width=20).grid(row=1, column=i, pady=10)
        # 添加确定和取消按钮
        b_frame = tk.Frame(child_window, bd=2, relief='groove')
        b_frame.pack(side='bottom', fill='both', expand=True)
        tk.Button(b_frame, text='Confirm', width=10, command=confirm).pack(side='left')
        tk.Button(b_frame, text='Cancel', width=10, command=cancel).pack(side='right')

    def search_course_choosing():  # 用课程ID或名称查询选课情况，表Course Choosing
        def confirm():
            id = value_list[0].get()
            name = value_list[1].get()
            record = [(id,)]
            if len(id) > 0 and len(name) > 0:  # 既有ID又有课程名称输入
                record = cursor.select(f"SELECT ID FROM Course WHERE Name='{name}'")  # 用名字查该课程的ID号
                if id != record[0][0]:
                    messagebox.showwarning(title="Inconsistent Input", message="Please check that ID"
                                                                               " and Name is correct.")
                    return 0  # 不兼容的输入，直接结束
            # 这里之后只有兼容的输入，没有条件，只有ID或只有名称，或者兼容的ID和名称
            elif len(id) == 0 and len(name) > 0:  # 只有名称的输入
                record = cursor.select(f"SELECT ID FROM Course WHERE Name='{name}'")  # 用名字查该课程的ID号
            condition = 'Course_ID=' + record[0][0]
            if len(condition) > 10:
                sql = "Select S.Name, C2.Name, T.Name, C1.Chosen_Year, C1.Score " \
                      "FROM Course_Choosing as C1, Course as C2, Student as S, Teacher as T " \
                      "WHERE " + condition + " and C1.Course_ID=C2.ID and C1.Student_ID=S.ID and C1.Teacher_ID=T.ID"
            else:
                sql = "Select S.Name, C2.Name, T.Name, C1.Chosen_Year, C1.Score " \
                      "FROM Course_Choosing as C1, Course as C2, Student as S, Teacher as T " \
                      "WHERE C1.Course_ID=C2.ID and C1.Student_ID=S.ID and C1.Teacher_ID=T.ID"
            result = cursor.select(sql)
            column_list = ['Student Name', 'Course Name', 'Teacher Name', 'Chosen Year', 'Score']
            wd = table_width[1] // len(column_list)  # 平均列宽
            table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
            for column in column_list:
                table.heading(column, text=column)
                table.column(column, width=wd, minwidth=wd, anchor="center")
            for i, record in enumerate(result):
                table.insert('', index=i, values=record)
            current_table[0].destroy()  # 删除原来的表
            current_table[0] = table  # 记录当前表
            table.grid(row=1, column=0, sticky='w')

        def cancel():
            child_window.destroy()

        idx = choice.get()
        column_list = ['Course ID', 'Course Name']
        child_window = tk.Toplevel(mis)  # 创建一个子窗口
        child_window.title('Search courses from current table ' + list(DatabaseTable.keys())[idx])
        child_window.geometry('+%d+%d' % (int((screen_size[0] - child_window.winfo_reqwidth()) / 2) - 100,
                                          (int((screen_size[1] - child_window.winfo_reqheight()) / 2))))
        main_frame = tk.Frame(child_window, bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True)
        value_list = [tk.StringVar() for i in range(len(column_list))]
        for i, column in enumerate(column_list):  # 放置条件输入框，conditions
            tk.Label(main_frame, text=column, font=("Times New Roman", 12), width=20).grid(row=0, column=i, pady=10)
            tk.Entry(main_frame, textvariable=value_list[i], width=20).grid(row=1, column=i, pady=10)
        # 添加确定和取消按钮
        b_frame = tk.Frame(child_window, bd=2, relief='groove')
        b_frame.pack(side='bottom', fill='both', expand=True)
        tk.Button(b_frame, text='Confirm', width=10, command=confirm).pack(side='left')
        tk.Button(b_frame, text='Cancel', width=10, command=cancel).pack(side='right')

    def search_teaches():  # 用老师ID或名字查询老师教的课，表Teaches
        def confirm():
            id = value_list[0].get()
            name = value_list[1].get()
            record = [(id,)]
            if len(id) > 0 and len(name) > 0:  # 既有ID又有名称输入
                record = cursor.select(f"SELECT ID FROM Teacher WHERE Name='{name}'")  # 用名字查该老师的ID号
                if id != record[0][0]:
                    messagebox.showwarning(title="Inconsistent Input", message="Please check that ID"
                                                                               " and Name is correct.")
                    return 0  # 不兼容的输入，直接结束
            # 这里之后只有兼容的输入，没有条件，只有ID或只有名称，或者兼容的ID和名称
            elif len(id) == 0 and len(name) > 0:  # 只有名称的输入
                record = cursor.select(f"SELECT ID FROM Teacher WHERE Name='{name}'")  # 用名字查该老师的ID号
            condition = 'T1.Teacher_ID=' + record[0][0]
            if len(condition) > 14:
                sql = "Select T2.Name, C.Name FROM Teaches as T1, Teacher as T2, Course as C " \
                      "WHERE " + condition + " and T1.Teacher_ID=T2.ID and T1.Course_ID=C.ID"
            else:
                sql = "Select T2.Name, C.Name FROM Teaches as T1, Teacher as T2, Course as C " \
                      "WHERE T1.Teacher_ID=T2.ID and T1.Course_ID=C.ID"
            result = cursor.select(sql)
            column_list = ['Teacher Name', 'Course Name']
            wd = table_width[1] // len(column_list)  # 平均列宽
            table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
            for column in column_list:
                table.heading(column, text=column)
                table.column(column, width=wd, minwidth=wd, anchor="center")
            for i, record in enumerate(result):
                table.insert('', index=i, values=record)
            current_table[0].destroy()  # 删除原来的表
            current_table[0] = table  # 记录当前表
            table.grid(row=1, column=0, sticky='w')

        def cancel():
            child_window.destroy()

        idx = choice.get()
        column_list = ['Teacher ID', 'Teacher Name']
        child_window = tk.Toplevel(mis)  # 创建一个子窗口
        child_window.title('Search courses from current table ' + list(DatabaseTable.keys())[idx])
        child_window.geometry('+%d+%d' % (int((screen_size[0] - child_window.winfo_reqwidth()) / 2) - 100,
                                          (int((screen_size[1] - child_window.winfo_reqheight()) / 2))))
        main_frame = tk.Frame(child_window, bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True)
        value_list = [tk.StringVar() for i in range(len(column_list))]
        for i, column in enumerate(column_list):  # 放置条件输入框，conditions
            tk.Label(main_frame, text=column, font=("Times New Roman", 12), width=20).grid(row=0, column=i, pady=10)
            tk.Entry(main_frame, textvariable=value_list[i], width=20).grid(row=1, column=i, pady=10)
        # 添加确定和取消按钮
        b_frame = tk.Frame(child_window, bd=2, relief='groove')
        b_frame.pack(side='bottom', fill='both', expand=True)
        tk.Button(b_frame, text='Confirm', width=10, command=confirm).pack(side='left')
        tk.Button(b_frame, text='Cancel', width=10, command=cancel).pack(side='right')

    def search_average3():
        column_list = ['Class', 'Course Name', 'Average Score']
        wd = table_width[1] // len(column_list)  # 平均列宽
        table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
        for column in column_list:
            table.heading(column, text=column)
            table.column(column, width=wd, minwidth=wd, anchor="center")
        sql = "select Class, Ce.Name, AVG(Score) as Avgerage_Score " \
              "from Course_Choosing as C, Student as S, Course as Ce " \
              "where C.Student_ID = S.ID and C.Course_ID = Ce.ID " \
              "group by Ce.Name, Class"
        result = cursor.select(sql)
        for i, record in enumerate(result):
            table.insert('', index=i, values=record)
        current_table[0].destroy()  # 删除原来的表
        current_table[0] = table  # 记录当前表
        table.grid(row=1, column=0, sticky='w')

    # 基础界面
    table_list_frame = tk.Frame(mis, bd=2, relief='groove')
    table_list_frame.pack(side='left', fill='y', expand=True)
    choice = tk.IntVar()
    tk.Label(table_list_frame, text="Tables", font=("Times New Roman", 12), width=15,
             background='lightskyblue').grid(row=0, column=0)
    for index, key in enumerate(DatabaseTable.keys()):  # 为所有表创建选择键
        if key != 'Account' and key != 'Student':
            tk.Radiobutton(table_list_frame, highlightcolor='blue', text=key,
                           variable=choice, value=index, anchor='w', indicatoron=False,
                           font=("Times New Roman", 12), width=15, command=choose_table).grid(row=index + 1, column=0)
    # 表内容子窗口
    content_frame = tk.Frame(mis, bd=2, relief='groove')
    content_frame.pack(side='left', fill='both', expand=True)
    content_label = tk.Label(content_frame, text="Content", font=("Times New Roman", 12), width=50,
                             background='lightskyblue')
    content_label.grid(row=0, column=0, sticky='w')
    # 功能键子窗口
    button_frame = tk.Frame(mis, bd=2, relief='groove')
    button_frame.pack(side='left', fill='y', expand=True)
    tk.Label(button_frame, text="Functions", font=("Times New Roman", 12), background='lightskyblue', width=12).grid(
        row=0, column=0)
    update = tk.Button(button_frame, text="Update", width=12, command=update)
    # 查询功能键
    search_teacher = tk.Button(button_frame, text="Search teacher", width=12, command=search_course)
    search_teaches = tk.Button(button_frame, text="Search teaches", width=12, command=search_teaches)
    search_course = tk.Button(button_frame, text="Search course", width=12, command=search_course)
    search_course_choosing = tk.Button(button_frame, text="Search\ncourse\nchoosing", width=12,
                                       command=search_course_choosing)
    search_average3 = tk.Button(button_frame, text="Average score\nof a course\nand a class", width=12, command=search_average3)
    # 初始化
    choose_table()  # 获得当前表
    mis.bind('<Configure>', scale)  # 将屏幕大小变化事件和控件大小变化事件绑定在一起
    mis.mainloop()


# ---------------------------------------------------------------------------------------------------------------


def mis_window_of_administrator():  # 管理员的窗口
    mise.destroy()
    mis = tk.Tk()  # 创建第二个窗口
    wt, ht = 720, 480
    centerx, centery = int((screen_size[0] - width) / 2), int((screen_size[1] - height) / 2) - 200  # 计算左上角坐标
    mis.title("Management Information System")
    mis.geometry('%dx%d+%d+%d' % (wt, ht, centerx, centery))
    mis.update()
    timestamp1 = [time.time()]
    timestamp2 = [time.time()]
    mis_saved_width = [wt]
    table_width = [450, 450]  # [0]为旧值，[1]为新值
    current_table = []

    def scale(event):
        table_width[0] = table_width[1]  # 记录旧值
        table_width[1] += mis.winfo_width() - mis_saved_width[0]  # 重新设置表的宽度
        mis_saved_width[0] = mis.winfo_width()
        content_label.config(width=int(table_width[0]//9))
        timestamp2[0] = time.time()
        # 只有表宽度变化的时候才调用choose_table，否则可能覆盖结果。用时间差限制函数的多次调用
        if table_width[0] - table_width[1] != 0 and \
                timestamp2[0] - timestamp1[0] >= 0.5:
            choose_table()
        timestamp1[0] = time.time()

    def show_search_result(result):
        idx = choice.get()
        column_list = DatabaseTable[list(DatabaseTable.keys())[idx]]
        wd = table_width[1] // len(column_list)  # 平均列宽
        table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
        for column in column_list:
            table.heading(column, text=column)
            table.column(column, width=wd, minwidth=wd, anchor="center")
        for i, record in enumerate(result):
            table.insert('', index=i, values=record)
        current_table[0].destroy()  # 删除原来的表
        current_table[0] = table  # 记录当前表
        table.grid(row=1, column=0, sticky='w')

    def choose_table():
        idx = choice.get()
        if idx == 0:  # Student
            search_student.grid(row=4, column=0)
            search_score.grid_forget()
            search_course.grid_forget()
            search_teacher.grid_forget()
            search_teaches.grid_forget()
            search_course_choosing.grid_forget()
            search_average.grid_forget()
            search_average2.grid_forget()
            search_average3.grid_forget()
        elif idx == 1:  # Course
            search_student.grid_forget()
            search_score.grid_forget()
            search_course.grid(row=4, column=0)
            search_teacher.grid_forget()
            search_teaches.grid_forget()
            search_course_choosing.grid_forget()
            search_average.grid_forget()
            search_average2.grid_forget()
            search_average3.grid_forget()
        elif idx == 2:  # Teacher
            search_student.grid_forget()
            search_score.grid_forget()
            search_course.grid_forget()
            search_teacher.grid(row=4, column=0)
            search_teaches.grid_forget()
            search_course_choosing.grid_forget()
            search_average.grid_forget()
            search_average2.grid_forget()
            search_average3.grid_forget()
        elif idx == 3:  # Teaches
            search_student.grid_forget()
            search_score.grid_forget()
            search_course.grid_forget()
            search_teacher.grid_forget()
            search_teaches.grid(row=4, column=0)
            search_course_choosing.grid_forget()
            search_average.grid_forget()
            search_average2.grid_forget()
            search_average3.grid_forget()
        elif idx == 4:  # Course choosing
            search_student.grid_forget()
            search_score.grid(row=4, column=0)
            search_course.grid_forget()
            search_teacher.grid_forget()
            search_teaches.grid_forget()
            search_course_choosing.grid(row=5, column=0)
            search_average.grid(row=6, column=0)
            search_average2.grid(row=7, column=0)
            search_average3.grid(row=8, column=0)
        else:
            search_student.grid_forget()
            search_score.grid_forget()
            search_course.grid_forget()
            search_teacher.grid_forget()
            search_teaches.grid_forget()
            search_course_choosing.grid_forget()
            search_average.grid_forget()
            search_average2.grid_forget()
            search_average3.grid_forget()
        column_list = DatabaseTable[list(DatabaseTable.keys())[idx]]
        wd = table_width[1]//len(column_list)  # 平均列宽
        table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
        for column in column_list:
            table.heading(column, text=column)
            table.column(column, width=wd, minwidth=wd, anchor="center")
        result = cursor.select('SELECT * FROM ' + list(DatabaseTable.keys())[idx])  # 查询表
        for i, record in enumerate(result):
            table.insert('', index=i, values=record)
        if len(current_table) == 0:  # 初始化
            current_table.append(table)
        else:
            current_table[0].destroy()  # 删除原来的表
            current_table[0] = table  # 记录当前表
        table.grid(row=1, column=0, sticky='w')

    def insert_record():  # 插入功能界面
        def confirm():
            record = [value_list[i].get() for i in range(len(value_list))]  # 获取结果，查表中列的类型，不是string就是int
            insert_list = []
            types = DatabaseColumnTypes[list(DatabaseTable.keys())[idx]]  # 获得当前表的每一列的类型，进行类型检查
            for i, tp in enumerate(types):
                if len(record[i]) != 0:  # 输入不为空
                    insert_list.append(i + 1)
                    if tp == 'int':  # 转换成int
                        record[i] = int(record[i])
            if len(insert_list) != 0:  # 输入不全为空
                a = len(insert_list) - 1
                for i in range(len(record) - 1, -1, -1):  # 倒序删减
                    if i != insert_list[a] - 1:  # 输入为空的列
                        record.pop(i)
                    else:  # 找下一个输入不为空的列的序号
                        a -= 1
                        if a < 0:
                            break
                cursor.insert(list(DatabaseTable.keys())[idx], insert_list, [record])  # 插入
                choose_table()  # 展示结果
            else:
                messagebox.showwarning(title="Empty Input Warning", message="No valid input, please check input.")

        def cancel():
            child_window.destroy()

        idx = choice.get()
        column_list = DatabaseTable[list(DatabaseTable.keys())[idx]]
        child_window = tk.Toplevel(mis)  # 创建一个子窗口
        child_window.title('Insert a record into current table ' + list(DatabaseTable.keys())[idx])
        child_window.geometry('+%d+%d' % (int((screen_size[0] - child_window.winfo_reqwidth()) / 2) - 100,
                                          (int((screen_size[1] - child_window.winfo_reqheight()) / 2))))
        main_frame = tk.Frame(child_window, bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True)
        value_list = [tk.StringVar() for i in range(len(column_list))]
        for i, column in enumerate(column_list):  # 放置输入框
            tk.Label(main_frame, text=column, font=("Times New Roman", 12), width=20).grid(row=0, column=i, pady=10)
            if idx == 4 and i == 4:  # 第五张表Course_Choosing的第五个属性Score
                tk.Label(main_frame, font=("Times New Roman", 12), width=20).grid(row=1, column=i, pady=10)
            else:
                tk.Entry(main_frame, textvariable=value_list[i], width=20).grid(row=1, column=i, pady=10)
        # 添加确定和取消按钮
        b_frame = tk.Frame(child_window, bd=2, relief='groove')
        b_frame.pack(side='bottom', fill='both', expand=True)
        tk.Button(b_frame, text='Confirm', width=10, command=confirm).pack(side='left')
        tk.Button(b_frame, text='Cancel', width=10, command=cancel).pack(side='right')

    def delete():  # 删除功能界面
        def confirm():
            record = [value_list[i].get() for i in range(len(value_list))]  # 获取where条件，做字符串and连接处理和加引号处理
            names = DatabaseTable[list(DatabaseTable.keys())[idx]]  # 获取当前表的每一列的名字
            types = DatabaseColumnTypes[list(DatabaseTable.keys())[idx]]  # 获得当前表的每一列的类型，进行类型检查，加引号
            condition = ''
            for i in range(len(record)):  # where语句条件
                if len(record[i]) != 0:  # 输入不为空
                    if len(condition) == 0:
                        condition += list(DatabaseTable.keys())[idx] + '.' + names[i] + combobox_list[i].get()
                        if types[i] == 'int':
                            condition += record[i]
                        else:
                            condition += "'" + record[i] + "'"  # 对string类型加双引号
                    else:
                        condition += ' and ' + list(DatabaseTable.keys())[idx] + '.' + names[i] + combobox_list[i].get()
                        if types[i] == 'int':
                            condition += record[i]
                        else:
                            condition += "'" + record[i] + "'"  # 对string类型加双引号
            if len(condition) != 0:
                cursor.delete(list(DatabaseTable.keys())[idx], condition)
                choose_table()  # 展示结果
            else:
                messagebox.showwarning(title="Empty Input Warning", message="No valid input, please check input.")

        def cancel():
            child_window.destroy()

        idx = choice.get()
        column_list = DatabaseTable[list(DatabaseTable.keys())[idx]]
        child_window = tk.Toplevel(mis)  # 创建一个子窗口
        child_window.title('Delete records from current table ' + list(DatabaseTable.keys())[idx])
        child_window.geometry('+%d+%d' % (int((screen_size[0] - child_window.winfo_reqwidth()) / 2) - 100,
                                          (int((screen_size[1] - child_window.winfo_reqheight()) / 2))))
        main_frame = tk.Frame(child_window, bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True)
        value_list = [tk.StringVar() for i in range(len(column_list))]
        combobox_list = []
        for i, column in enumerate(column_list):  # 放置条件输入框，conditions
            tk.Label(main_frame, text=column, font=("Times New Roman", 12), width=20).grid(row=0, column=i, pady=10)
            tk.Entry(main_frame, textvariable=value_list[i], width=20).grid(row=2, column=i, pady=10)
            combo = ttk.Combobox(main_frame, values=('=', '<', '>', '>=', '<='), state='readonly',
                                 font=("Times New Roman", 12), cursor='arrow', width=5)
            combobox_list.append(combo)
            combo.grid(row=1, column=i)
        # 添加确定和取消按钮
        b_frame = tk.Frame(child_window, bd=2, relief='groove')
        b_frame.pack(side='bottom', fill='both', expand=True)
        tk.Button(b_frame, text='Confirm', width=10, command=confirm).pack(side='left')
        tk.Button(b_frame, text='Cancel', width=10, command=cancel).pack(side='right')

    def update():  # 修改功能界面
        def confirm():
            # 获取where条件，做字符串and连接处理和加引号处理
            record = [condition_value_list[i].get() for i in range(len(condition_value_list))]
            names = DatabaseTable[list(DatabaseTable.keys())[idx]]  # 获取当前表的每一列的名字
            types = DatabaseColumnTypes[list(DatabaseTable.keys())[idx]]  # 获得当前表的每一列的类型，进行类型检查，加引号
            condition = ''
            for i in range(len(record)):  # where语句条件
                if len(record[i]) != 0:  # 输入不为空
                    if len(condition) == 0:
                        condition += list(DatabaseTable.keys())[idx] + '.' + names[i] + combobox_list[i].get()
                        if types[i] == 'int':
                            condition += record[i]
                        else:
                            condition += "'" + record[i] + "'"  # 对string类型加双引号
                    else:
                        condition += ' and ' + list(DatabaseTable.keys())[idx] + '.' + names[i] + combobox_list[i].get()
                        if types[i] == 'int':
                            condition += record[i]
                        else:
                            condition += "'" + record[i] + "'"  # 对string类型加双引号
            # 获取修改值，并做加逗号分隔处理
            new_record = [new_value_list[i].get() for i in range(len(new_value_list))]
            set_clause = ''
            for i in range(len(new_record)):  # where语句条件
                if len(new_record[i]) != 0:  # 输入不为空
                    if len(set_clause) == 0:
                        set_clause += list(DatabaseTable.keys())[idx] + '.' + names[i] + '='
                        if types[i] == 'int':
                            set_clause += new_record[i]
                        else:
                            set_clause += "'" + new_record[i] + "'"  # 对string类型加双引号
                    else:
                        set_clause += ', ' + list(DatabaseTable.keys())[idx] + '.' + names[i] + '='  # 逗号分隔
                        if types[i] == 'int':
                            set_clause += new_record[i]
                        else:
                            set_clause += "'" + new_record[i] + "'"  # 对string类型加双引号
            if len(condition) != 0 and len(set_clause) != 0:  # 两个都不为空才能修改
                cursor.update(list(DatabaseTable.keys())[idx], set_clause, condition)
                choose_table()  # 展示结果
            else:
                messagebox.showwarning(title="Empty Input or Condition Warning", message="No valid input or condition, please check input or condition.")

        def cancel():
            child_window.destroy()

        idx = choice.get()
        column_list = DatabaseTable[list(DatabaseTable.keys())[idx]]  # 当前表列名
        child_window = tk.Toplevel(mis)  # 创建一个子窗口
        child_window.title('Update records in the current table ' + list(DatabaseTable.keys())[idx])
        child_window.geometry('+%d+%d' % (int((screen_size[0] - child_window.winfo_reqwidth()) / 2) - 100,
                                          (int((screen_size[1] - child_window.winfo_reqheight()) / 2))))
        main_frame = tk.Frame(child_window, bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True)
        new_value_list = [tk.StringVar() for i in range(len(column_list))]  # 修改值的value列表
        condition_value_list = [tk.StringVar() for i in range(len(column_list))]  # 条件框的value列表
        combobox_list = []
        tk.Label(main_frame, text='New value:', font=("Times New Roman", 12), width=10).grid(row=1, column=0, pady=10)
        tk.Label(main_frame, text='Conditions:', font=("Times New Roman", 12), width=10).grid(row=3, column=0, pady=10)
        for i, column in enumerate(column_list):  # 放置条件输入框，conditions
            tk.Label(main_frame, text=column, font=("Times New Roman", 12), width=20).grid(row=0, column=i + 1, pady=10)
            if idx == 4 and i == 4:  # Score
                tk.Label(main_frame, font=("Times New Roman", 12), width=20).grid(row=1, column=i + 1, pady=10)
            else:
                tk.Entry(main_frame, textvariable=new_value_list[i], width=20).grid(row=1, column=i + 1, pady=10)  # 修改值输入框
            tk.Entry(main_frame, textvariable=condition_value_list[i], width=20).grid(row=3, column=i + 1, pady=10)  # 条件值输入框
            combo = ttk.Combobox(main_frame, values=('=', '<', '>', '>=', '<='), state='readonly',
                                 font=("Times New Roman", 12), cursor='arrow', width=5)
            combobox_list.append(combo)
            combo.grid(row=2, column=i + 1)

        # 添加确定和取消按钮
        b_frame = tk.Frame(child_window, bd=2, relief='groove')
        b_frame.pack(side='bottom', fill='both', expand=True)
        tk.Button(b_frame, text='Confirm', width=10, command=confirm).pack(side='left')
        tk.Button(b_frame, text='Cancel', width=10, command=cancel).pack(side='right')

    def search_score():  # 用学生ID或名字和课程ID或名称查选课信息和分数
        def confirm():
            attribute1 = combobox_list[0].get()
            attribute2 = combobox_list[1].get()
            if len(attribute1) == 0 and len(attribute2) == 0:
                sql = f"SELECT S.Name, C2.Name, T.Name, C1.Score " \
                      f"FROM Course_Choosing as C1, Student as S, Course as C2, Teacher as T" \
                      f" WHERE C1.Student_ID=S.ID and C1.Course_ID=C2.ID and C1.Teacher_ID=T.ID"
                result = cursor.select(sql)
                column_list = ['Student Name', 'Course Name', 'Teacher Name', 'Score']
                wd = table_width[1] // len(column_list)  # 平均列宽
                table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
                for column in column_list:
                    table.heading(column, text=column)
                    table.column(column, width=wd, minwidth=wd, anchor="center")
                for i, record in enumerate(result):
                    table.insert('', index=i, values=record)
                current_table[0].destroy()  # 删除原来的表
                current_table[0] = table  # 记录当前表
                table.grid(row=1, column=0, sticky='w')
                return 0
            record = [value_list[i].get() for i in range(len(value_list))]  # 获取where条件，做字符串and连接处理和加引号处理
            types = DatabaseColumnTypes[list(DatabaseTable.keys())[idx]]  # 获得当前表的每一列的类型，进行类型检查，加引号
            condition = ''
            for i in range(len(record)):  # where语句条件
                if len(record[i]) != 0:  # 输入不为空
                    if i == 0:
                        a = 'S.'
                    else:
                        a = 'C2.'
                    if len(condition) == 0:
                        condition += a + combobox_list[i].get() + '='
                        if types[i] == 'int':
                            condition += record[i]
                        else:
                            condition += "'" + record[i] + "'"  # 对string类型加双引号
                    else:
                        condition += f' and {a}' + combobox_list[i].get() + '='
                        if types[i] == 'int':
                            condition += record[i]
                        else:
                            condition += "'" + record[i] + "'"  # 对string类型加双引号
            if len(condition) != 0:
                sql = f"SELECT S.Name, C2.Name, T.Name, C1.Score " \
                      f"FROM Course_Choosing as C1, Student as S, Course as C2, Teacher as T"\
                      f" WHERE {condition} and "\
                      f"C1.Student_ID=S.ID and C1.Course_ID=C2.ID and C1.Teacher_ID=T.ID"
            else:
                sql = f"SELECT S.Name, C2.Name, T.Name, C1.Score " \
                      f"FROM Course_Choosing as C1, Student as S, Course as C2, Teacher as T" \
                      f" WHERE C1.Student_ID=S.ID and C1.Course_ID=C2.ID and C1.Teacher_ID=T.ID"
            result = cursor.select(sql)
            column_list = ['Student Name', 'Course Name', 'Teacher Name', 'Score']
            wd = table_width[1] // len(column_list)  # 平均列宽
            table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
            for column in column_list:
                table.heading(column, text=column)
                table.column(column, width=wd, minwidth=wd, anchor="center")
            for i, record in enumerate(result):
                table.insert('', index=i, values=record)
            current_table[0].destroy()  # 删除原来的表
            current_table[0] = table  # 记录当前表
            table.grid(row=1, column=0, sticky='w')

        def cancel():
            child_window.destroy()

        idx = choice.get()
        column_list = ['Student Information', 'Course Information']
        child_window = tk.Toplevel(mis)  # 创建一个子窗口
        child_window.title('Search scores from current table ' + list(DatabaseTable.keys())[idx])
        child_window.geometry('+%d+%d' % (int((screen_size[0] - child_window.winfo_reqwidth()) / 2) - 100,
                                          (int((screen_size[1] - child_window.winfo_reqheight()) / 2))))
        main_frame = tk.Frame(child_window, bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True)
        value_list = [tk.StringVar() for i in range(len(column_list))]
        combobox_list = []
        for i, column in enumerate(column_list):  # 放置条件输入框，conditions
            tk.Label(main_frame, text=column, font=("Times New Roman", 12), width=20).grid(row=0, column=i, pady=10)
            tk.Entry(main_frame, textvariable=value_list[i], width=20).grid(row=2, column=i, pady=10)
            combo = ttk.Combobox(main_frame, values=('ID', 'Name'), state='readonly',
                                 font=("Times New Roman", 12), cursor='arrow', width=5)
            combobox_list.append(combo)
            combo.grid(row=1, column=i)
        # 添加确定和取消按钮
        b_frame = tk.Frame(child_window, bd=2, relief='groove')
        b_frame.pack(side='bottom', fill='both', expand=True)
        tk.Button(b_frame, text='Confirm', width=10, command=confirm).pack(side='left')
        tk.Button(b_frame, text='Cancel', width=10, command=cancel).pack(side='right')

    def search_course():  # 用课程ID或名称查询课程信息，表Course
        def confirm():
            record = [value_list[i].get() for i in range(len(value_list))]  # 获取where条件，做字符串and连接处理和加引号处理
            names = DatabaseTable[list(DatabaseTable.keys())[idx]]  # 获取当前表的每一列的名字
            types = DatabaseColumnTypes[list(DatabaseTable.keys())[idx]]  # 获得当前表的每一列的类型，进行类型检查，加引号
            condition = ''
            for i in range(len(record)):  # where语句条件
                if len(record[i]) != 0:  # 输入不为空
                    if len(condition) == 0:  # 第一个条件
                        condition += list(DatabaseTable.keys())[idx] + '.' + names[i] + '='
                        if types[i] == 'int':
                            condition += record[i]
                        else:
                            condition += "'" + record[i] + "'"  # 对string类型加双引号
                    else:
                        condition += ' and ' + list(DatabaseTable.keys())[idx] + '.' + names[i] + '='
                        if types[i] == 'int':
                            condition += record[i]
                        else:
                            condition += "'" + record[i] + "'"  # 对string类型加双引号
            if len(condition) != 0:
                result = cursor.select("Select * FROM " + list(DatabaseTable.keys())[idx] + " WHERE " + condition)
                show_search_result(result)  # 展示查询结果
            else:
                choose_table()  # 默认显示所有课程的信息

        def cancel():
            child_window.destroy()

        idx = choice.get()
        column_list = DatabaseTable[list(DatabaseTable.keys())[idx]][:2]  # 前两项ID、Name
        child_window = tk.Toplevel(mis)  # 创建一个子窗口
        child_window.title('Search courses from current table ' + list(DatabaseTable.keys())[idx])
        child_window.geometry('+%d+%d' % (int((screen_size[0] - child_window.winfo_reqwidth()) / 2) - 100,
                                          (int((screen_size[1] - child_window.winfo_reqheight()) / 2))))
        main_frame = tk.Frame(child_window, bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True)
        value_list = [tk.StringVar() for i in range(len(column_list))]
        for i, column in enumerate(column_list):  # 放置条件输入框，conditions
            tk.Label(main_frame, text=column, font=("Times New Roman", 12), width=20).grid(row=0, column=i, pady=10)
            tk.Entry(main_frame, textvariable=value_list[i], width=20).grid(row=1, column=i, pady=10)
        # 添加确定和取消按钮
        b_frame = tk.Frame(child_window, bd=2, relief='groove')
        b_frame.pack(side='bottom', fill='both', expand=True)
        tk.Button(b_frame, text='Confirm', width=10, command=confirm).pack(side='left')
        tk.Button(b_frame, text='Cancel', width=10, command=cancel).pack(side='right')

    def search_course_choosing():  # 用课程ID或名称查询选课情况，表Course Choosing
        def confirm():
            id = value_list[0].get()
            name = value_list[1].get()
            record = [(id,)]
            if len(id) > 0 and len(name) > 0:  # 既有ID又有课程名称输入
                record = cursor.select(f"SELECT ID FROM Course WHERE Name='{name}'")  # 用名字查该课程的ID号
                if id != record[0][0]:
                    messagebox.showwarning(title="Inconsistent Input", message="Please check that ID"
                                                                               " and Name is correct.")
                    return 0  # 不兼容的输入，直接结束
            # 这里之后只有兼容的输入，没有条件，只有ID或只有名称，或者兼容的ID和名称
            elif len(id) == 0 and len(name) > 0:  # 只有名称的输入
                record = cursor.select(f"SELECT ID FROM Course WHERE Name='{name}'")  # 用名字查该课程的ID号
            condition = 'Course_ID=' + record[0][0]
            if len(condition) > 10:
                sql = "Select S.Name, C2.Name, T.Name, C1.Chosen_Year, C1.Score " \
                      "FROM Course_Choosing as C1, Course as C2, Student as S, Teacher as T " \
                      "WHERE " + condition + " and C1.Course_ID=C2.ID and C1.Student_ID=S.ID and C1.Teacher_ID=T.ID"
            else:
                sql = "Select S.Name, C2.Name, T.Name, C1.Chosen_Year, C1.Score " \
                      "FROM Course_Choosing as C1, Course as C2, Student as S, Teacher as T " \
                      "WHERE C1.Course_ID=C2.ID and C1.Student_ID=S.ID and C1.Teacher_ID=T.ID"
            result = cursor.select(sql)
            column_list = ['Student Name', 'Course Name', 'Teacher Name', 'Chosen Year', 'Score']
            wd = table_width[1] // len(column_list)  # 平均列宽
            table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
            for column in column_list:
                table.heading(column, text=column)
                table.column(column, width=wd, minwidth=wd, anchor="center")
            for i, record in enumerate(result):
                table.insert('', index=i, values=record)
            current_table[0].destroy()  # 删除原来的表
            current_table[0] = table  # 记录当前表
            table.grid(row=1, column=0, sticky='w')

        def cancel():
            child_window.destroy()

        idx = choice.get()
        column_list = ['Course ID', 'Course Name']
        child_window = tk.Toplevel(mis)  # 创建一个子窗口
        child_window.title('Search courses from current table ' + list(DatabaseTable.keys())[idx])
        child_window.geometry('+%d+%d' % (int((screen_size[0] - child_window.winfo_reqwidth()) / 2) - 100,
                                          (int((screen_size[1] - child_window.winfo_reqheight()) / 2))))
        main_frame = tk.Frame(child_window, bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True)
        value_list = [tk.StringVar() for i in range(len(column_list))]
        for i, column in enumerate(column_list):  # 放置条件输入框，conditions
            tk.Label(main_frame, text=column, font=("Times New Roman", 12), width=20).grid(row=0, column=i, pady=10)
            tk.Entry(main_frame, textvariable=value_list[i], width=20).grid(row=1, column=i, pady=10)
        # 添加确定和取消按钮
        b_frame = tk.Frame(child_window, bd=2, relief='groove')
        b_frame.pack(side='bottom', fill='both', expand=True)
        tk.Button(b_frame, text='Confirm', width=10, command=confirm).pack(side='left')
        tk.Button(b_frame, text='Cancel', width=10, command=cancel).pack(side='right')

    def search_teaches():  # 用老师ID或名字查询老师教的课，表Teaches
        def confirm():
            id = value_list[0].get()
            name = value_list[1].get()
            record = [(id,)]
            if len(id) > 0 and len(name) > 0:  # 既有ID又有名称输入
                record = cursor.select(f"SELECT ID FROM Teacher WHERE Name='{name}'")  # 用名字查该老师的ID号
                if id != record[0][0]:
                    messagebox.showwarning(title="Inconsistent Input", message="Please check that ID"
                                                                               " and Name is correct.")
                    return 0  # 不兼容的输入，直接结束
            # 这里之后只有兼容的输入，没有条件，只有ID或只有名称，或者兼容的ID和名称
            elif len(id) == 0 and len(name) > 0:  # 只有名称的输入
                record = cursor.select(f"SELECT ID FROM Teacher WHERE Name='{name}'")  # 用名字查该老师的ID号
            condition = 'T1.Teacher_ID=' + record[0][0]
            if len(condition) > 14:
                sql = "Select T2.Name, C.Name FROM Teaches as T1, Teacher as T2, Course as C " \
                      "WHERE " + condition + " and T1.Teacher_ID=T2.ID and T1.Course_ID=C.ID"
            else:
                sql = "Select T2.Name, C.Name FROM Teaches as T1, Teacher as T2, Course as C " \
                      "WHERE T1.Teacher_ID=T2.ID and T1.Course_ID=C.ID"
            result = cursor.select(sql)
            column_list = ['Teacher Name', 'Course Name']
            wd = table_width[1] // len(column_list)  # 平均列宽
            table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
            for column in column_list:
                table.heading(column, text=column)
                table.column(column, width=wd, minwidth=wd, anchor="center")
            for i, record in enumerate(result):
                table.insert('', index=i, values=record)
            current_table[0].destroy()  # 删除原来的表
            current_table[0] = table  # 记录当前表
            table.grid(row=1, column=0, sticky='w')

        def cancel():
            child_window.destroy()

        idx = choice.get()
        column_list = ['Teacher ID', 'Teacher Name']
        child_window = tk.Toplevel(mis)  # 创建一个子窗口
        child_window.title('Search courses from current table ' + list(DatabaseTable.keys())[idx])
        child_window.geometry('+%d+%d' % (int((screen_size[0] - child_window.winfo_reqwidth()) / 2) - 100,
                                          (int((screen_size[1] - child_window.winfo_reqheight()) / 2))))
        main_frame = tk.Frame(child_window, bd=2, relief='groove')
        main_frame.pack(fill='both', expand=True)
        value_list = [tk.StringVar() for i in range(len(column_list))]
        for i, column in enumerate(column_list):  # 放置条件输入框，conditions
            tk.Label(main_frame, text=column, font=("Times New Roman", 12), width=20).grid(row=0, column=i, pady=10)
            tk.Entry(main_frame, textvariable=value_list[i], width=20).grid(row=1, column=i, pady=10)
        # 添加确定和取消按钮
        b_frame = tk.Frame(child_window, bd=2, relief='groove')
        b_frame.pack(side='bottom', fill='both', expand=True)
        tk.Button(b_frame, text='Confirm', width=10, command=confirm).pack(side='left')
        tk.Button(b_frame, text='Cancel', width=10, command=cancel).pack(side='right')

    def search_average():
        column_list = ['Student Name', 'Average Score']
        wd = table_width[1] // len(column_list)  # 平均列宽
        table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
        for column in column_list:
            table.heading(column, text=column)
            table.column(column, width=wd, minwidth=wd, anchor="center")
        sql = "select S.Name, AVG(Score) as Average_Score " \
              "from Course_Choosing as C, Student as S " \
              "where C.Student_ID=S.ID " \
              "group by S.Name"
        result = cursor.select(sql)
        for i, record in enumerate(result):
            table.insert('', index=i, values=record)
        current_table[0].destroy()  # 删除原来的表
        current_table[0] = table  # 记录当前表
        table.grid(row=1, column=0, sticky='w')

    def search_average2():
        column_list = ['Average Score']
        wd = table_width[1] // len(column_list)  # 平均列宽
        table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
        for column in column_list:
            table.heading(column, text=column)
            table.column(column, width=wd, minwidth=wd, anchor="center")
        sql = "select AVG(Score) as Average_Score " \
              "from Course_Choosing"
        result = cursor.select(sql)
        for i, record in enumerate(result):
            table.insert('', index=i, values=record)
        current_table[0].destroy()  # 删除原来的表
        current_table[0] = table  # 记录当前表
        table.grid(row=1, column=0, sticky='w')

    def search_average3():
        column_list = ['Class', 'Course Name', 'Average Score']
        wd = table_width[1] // len(column_list)  # 平均列宽
        table = ttk.Treeview(content_frame, height=10, columns=column_list, show='headings')
        for column in column_list:
            table.heading(column, text=column)
            table.column(column, width=wd, minwidth=wd, anchor="center")
        sql = "select Class, Ce.Name, AVG(Score) as Avgerage_Score " \
              "from Course_Choosing as C, Student as S, Course as Ce " \
              "where C.Student_ID = S.ID and C.Course_ID = Ce.ID " \
              "group by Ce.Name, Class"
        result = cursor.select(sql)
        for i, record in enumerate(result):
            table.insert('', index=i, values=record)
        current_table[0].destroy()  # 删除原来的表
        current_table[0] = table  # 记录当前表
        table.grid(row=1, column=0, sticky='w')

    # 基础界面
    table_list_frame = tk.Frame(mis, bd=2, relief='groove')
    table_list_frame.pack(side='left', fill='y', expand=True)
    choice = tk.IntVar()
    tk.Label(table_list_frame, text="Tables", font=("Times New Roman", 12), width=15,
             background='lightskyblue').grid(row=0, column=0)
    for index, key in enumerate(DatabaseTable.keys()):  # 为所有表创建选择键
        # if key != 'Account':
        tk.Radiobutton(table_list_frame, highlightcolor='blue', text=key,
                       variable=choice, value=index, anchor='w', indicatoron=False,
                       font=("Times New Roman", 12), width=15, command=choose_table).grid(row=index + 1, column=0)
    # 表内容子窗口
    content_frame = tk.Frame(mis, bd=2, relief='groove')
    content_frame.pack(side='left', fill="y", anchor="w")
    content_label = tk.Label(content_frame, text="Content", font=("Times New Roman", 12),
                             width=50, background='lightskyblue')
    content_label.grid(row=0, column=0, sticky='w')
    # 功能键子窗口
    button_frame = tk.Frame(mis, bd=2, relief='groove')
    button_frame.pack(side='left', fill='y', expand=True)
    tk.Label(button_frame, text="Functions", font=("Times New Roman", 12), background='lightskyblue', width=12).grid(row=0, column=0)
    tk.Button(button_frame, text="Insert", width=12, command=insert_record).grid(row=1, column=0)
    tk.Button(button_frame, text="Delete", width=12, command=delete).grid(row=2, column=0)
    tk.Button(button_frame, text="Update", width=12, command=update).grid(row=3, column=0)
    # 查询功能键
    search_student = tk.Button(button_frame, text="Search student", width=12, command=search_course)
    search_score = tk.Button(button_frame, text="Search course\nand score", width=12, command=search_score)
    search_teacher = tk.Button(button_frame, text="Search teacher", width=12, command=search_course)
    search_teaches = tk.Button(button_frame, text="Search teaches", width=12, command=search_teaches)
    search_course = tk.Button(button_frame, text="Search course", width=12, command=search_course)
    search_course_choosing = tk.Button(button_frame, text="Search\ncourse\nchoosing", width=12, command=search_course_choosing)
    search_average = tk.Button(button_frame, text="Average\nscore 1", width=12, command=search_average)
    search_average2 = tk.Button(button_frame, text="Average\nscore 2", width=12, command=search_average2)
    search_average3 = tk.Button(button_frame, text="Average\nscore 3", width=12, command=search_average3)
    # 初始化
    choose_table()  # 获得当前表
    mis.bind('<Configure>', scale)  # 将屏幕大小变化事件和控件大小变化事件绑定在一起
    mis.mainloop()


def login():
    iden = identity.get()
    name = username.get()
    pwd = password.get()
    accounts = cursor.select("SELECT * FROM Account WHERE ID='" + name + "'" + " AND Identification='" + iden + "'")
    if len(accounts) == 0:
        messagebox.showwarning(title='Warning', message="No account is found")
    elif accounts[0][0] == name and accounts[0][1] == pwd:
        print("Sign up successfully")
        if iden == "Administrator":
            mis_window_of_administrator()
        elif iden == "Teacher":
            mis_window_of_teacher()
        else:
            mis_window_of_student()
    else:
        messagebox.showwarning(title="Warning", message="Fail to sign up, please check account and password")


def get_img(filename, width, height):
    img = Image.open(filename).resize((width, height))
    img = ImageTk.PhotoImage(img)
    return img


mise = tk.Tk()
mise.title("Management Information System Entry")
screen_size = [mise.winfo_screenwidth(), mise.winfo_screenheight()]  # 获取屏幕宽度和高度
width, height = 720, 330
x, y = int((screen_size[0] - width)/2), int((screen_size[1] - height)/2) - 100  # 计算左上角坐标
mise.geometry('%dx%d+%d+%d' % (width, height, x, y))
mise.resizable(False, False)  # 禁止最大化
cursor = DatabaseCursor(server='localhost', database='MyDatabase1', username='sa', password='123')
username = tk.StringVar()
password = tk.StringVar()
page = tk.Frame(mise, bd=1, relief='groove')  # 在根窗口上创建新的页
page.pack(fill='both', anchor="center")

image = get_img("../Image/Sign up page.png", 700, 70)
tk.Label(page, image=image).grid(row=0, column=0, columnspan=5, pady=20)
tk.Label(page, text="Welcome to Management Information System of Computer Science College of SCUT",
         font=("Times New Roman", 16)).grid(row=1, column=1, columnspan=3)

tk.Label(page, text="Identity", font=("Times New Roman", 12)).grid(row=2, column=1, pady=10)
identity = ttk.Combobox(page, values=('Administrator', 'Teacher', 'Student'), state='readonly',
                        font=("Times New Roman", 12), cursor='arrow', width=12)
identity.grid(row=2, column=2)

tk.Label(page, text="Account", font=("Times New Roman", 12)).grid(row=3, column=1, pady=10)
tk.Entry(page, textvariable=username).grid(row=3, column=2)

tk.Label(page, text="Password", font=("Times New Roman", 12)).grid(row=4, column=1, pady=10)
tk.Entry(page, textvariable=password).grid(row=4, column=2)

tk.Button(page, text="Sign up", command=login, width=10, font=("Times New Roman", 12)).grid(row=5, column=2, pady=10)
mise.mainloop()
