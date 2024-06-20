DatabaseTable = {'Student': ['ID', 'Name', 'Sex', 'Entrance_Age', 'Entrance_Year', 'Class'],
                 'Course': ['ID', 'Name', 'Teacher_ID', 'Credit', 'Grade', 'Canceled_Year'],
                 'Teacher': ['ID', 'Name'],
                 'Teaches': ['Teacher_ID', 'Course_ID'],
                 'Course_Choosing': ['Student_ID', 'Course_ID', 'Teacher_ID', 'Chosen_Year', 'Score'],
                 'Account': ['ID', 'Password', 'Identification']}  # Account记录登录账号和密码，不对外展示

DatabaseColumnTypes = {'Student': ['varchar(12)', 'varchar(20)', 'char(2)', 'int', 'int', 'varchar(40)'],
                       'Course': ['varchar(20)', 'varchar(20)', 'char(5)', 'int', 'varchar(10)', 'int'],
                       'Teacher': ['char(5)', 'varchar(20)'],
                       'Teaches': ['char(5)', 'varchar(10)'],
                       'Course_Choosing': ['char(12)', 'varchar(10)', 'char(5)', 'int', 'int'],
                       'Account': ['varchar(20)', 'varchar(20)', 'varchar(15)']}
