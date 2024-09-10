import sqlite3

### Connect to sqlite
connection = sqlite3.connect("Student.db")

### Create a curson object to insert record,create table
cursor = connection.cursor()

### Create a table
table_info = """
            create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT)
             """

cursor.execute(table_info)

### Insert some more records

cursor.execute('''Insert into STUDENT values('Anil','Gen AI','A+',95)''')
cursor.execute('''Insert into STUDENT values('Arjun','Data Science','A',90)''')
cursor.execute('''Insert into STUDENT values('Bunny','Devops','B',80)''')
cursor.execute('''Insert into STUDENT values('Gana','Machine Learning','A',92)''')

### Display all records
print("The Inserted records are:")
data = cursor.execute('''Select *from STUDENT''')

for row in data:
    r=print(row)

###Commit your changes in the database
connection.commit()
connection.close()