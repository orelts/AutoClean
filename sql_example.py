
import pyodbc
#connection command
conn = pyodbc.connect('Driver={SQL Server};'        #dont change
                      'Server=DESKTOP-N49DF0R;'     #server name can be parsed from name in the SQL SERVER MANAGEMENT
                      'Database=myFirstDatabase;'   #name of the database you want to parse from
                      'Trusted_Connection=yes;')    #dont change

cursor = conn.cursor()

#inserting a table , and afterwards adding a few subjects to that table
#insert table once only
cursor.execute('''

               CREATE TABLE sensors_table
               (
               Name nvarchar(50),
               population int,
               CapitalCity nvarchar(50)
               )

               ''')

conn.commit()
cursor.execute('''

                INSERT INTO myFirstDatabase.dbo.countries (Name, population, CapitalCity)
                VALUES
                ('Israel',10000000,'Jeruz'),
                ('Jordan',7,'Rabat'),
                ('Egypt',60000000,'Cairo')  

                ''')
conn.commit()

#extarcting a table and printing it
cursor.execute('SELECT * FROM myFirstDatabase.dbo.countries') #the text inside is SQL code

for row in cursor:
    print(row)

#deleting a table
cursor.execute('DROP TABLE countries')
conn.commit()