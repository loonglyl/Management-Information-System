# Management-Information-System
This is a management information system based on the SQL-server, which can connect to a remote SQL-server.

First, modify the SQL-server specified in ***UI.py***. 
>cursor = DatabaseCursor(server='localhost', database='MyDatabase1', username='sa', password='123')

1. The first parameter *server* is used to connect to a specific SQL-server.

2. The second parameter *database* is the name of a database created in your SQL-server. All information will be stored in this database.

3. The third parameter *username* is the default account 'sa' of a SQL-server.

4. The last parameter *password* is the password of this account.
Before using the system, we need to modify the password of default account ‘sa’ and then login in the way of SQL Server Authentication using this account.

Second, create accounts in SQL-server by adding records into a table named **Account**.

Then, this system can be used.
