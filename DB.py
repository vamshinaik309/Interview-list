import sqlite3

conn = sqlite3.connect('interviews.db')

c = conn.cursor()
c.execute('DROP TABLE if EXISTS interuser;')
c.execute('DROP TABLE if EXISTS interviews;')
c.execute('DROP TABLE if EXISTS users;')
c.execute('''
    CREATE table interviews(
        id integer PRIMARY KEY AUTOINCREMENT,
        name text,
        start datetime,
        end datetime
    );
''')
c.execute('''
    CREATE table users(
        id integer PRIMARY KEY AUTOINCREMENT,
        name text
    );
''')
c.execute('''
    CREATE table interuser(
        interviewid int FORIEGN KEY REFERENCES interviews(id),
        userid int FORIEGN KEY REFERENCES users(id)
    );
''')
c.execute('INSERT into users(name) values("karthik");')
c.execute('INSERT into users(name) values("malisetty");')
c.execute('INSERT into users(name) values("John");')
c.execute('INSERT into users(name) values("Doe");')
c.execute('INSERT into users(name) values("IDK");')

c.execute('INSERT into interviews(name, start, end) values("Interview1", "2020-10-05 10:00:00", "2020-10-05 12:00:00");')
c.execute('INSERT into interviews(name, start, end) values("Interview2", "2020-10-05 13:00:00", "2020-10-05 15:00:00");')
c.execute('INSERT into interviews(name, start, end) values("Interview3", "2020-10-05 11:00:00", "2020-10-05 12:30:00");')

c.execute('INSERT into interuser values(1,1);')
c.execute('INSERT into interuser values(1,2);')
c.execute('INSERT into interuser values(1,3);')
c.execute('INSERT into interuser values(2,1);')
c.execute('INSERT into interuser values(2,4);')
c.execute('INSERT into interuser values(2,5);')
c.execute('INSERT into interuser values(3,4);')
c.execute('INSERT into interuser values(3,5);')

conn.commit()
