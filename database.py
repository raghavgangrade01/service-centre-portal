import sqlite3
connection_object=sqlite3.connect("datacenter.db")
cursor=connection_object.cursor()
table='''
CREATE TABLE DATACENTER(
        Name Char(255) NOT NULL,
        Address VARCHAR(255) NOT NULL,
        Pincode INT NOT NULL,
        Category VARCHAR(255) NOT NULL,
        PaymentDetails VARCHAR(255) NOT NULL,
        PropriterName CHAR(255) NOT NULL,
        Phone CHAR(255) NOT NULL,
        Email VARCHAR(255) NOT NULL,
        City CHAR(255) NOT NULL,
        Username VARCHAR(255) NOT NULL,
        Password VARCHAR(255) NOT NULL
);'''

cursor.execute(table)
connection_object.close()