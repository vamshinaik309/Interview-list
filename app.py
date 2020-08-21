from flask import Flask, render_template, url_for, request, redirect
import sqlite3
app = Flask(__name__)

conn = sqlite3.connect('interviews.db', check_same_thread=False)
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


# def compatible((S, E), L):
#     for (e, s) in L:
#         if not ()


@app.route('/')
@app.route('/interviews-list')
def home():
    def getUsers(ID):
        c.execute(
            f'SELECT name from users where id in (SELECT userid from interuser where interviewid={ID});')
        st = []
        for x in c.fetchall():
            st.append(x[0])
        return st

    c.execute('SELECT * from interviews;')
    interviews = [{'id': x[0],
                   'name': x[1],
                   'users': getUsers(x[0]),
                   'start': x[2],
                   'end': x[3]} for x in c.fetchall()]
    return render_template('list.html', interviews=interviews)


@app.route('/create-interview', methods=['POST', 'GET'])
def createInterview():
    if request.method == 'POST':
        name = request.form['name']
        users = request.form['users'].split(';')
        start = request.form['start']
        end = request.form['end']
        if '' in [name, users, start, end]:
            return render_template('create.html', error="All fields are required")

        UID = []
        for user in users:
            print(f'-fffffffffffffffffff-{user}--')
            user = user.strip()
            with conn:
                c.execute(f'SELECT id from users where name="{user}";')
            temp = c.fetchone()
            if temp is not None:
                temp = temp[0]
                UID.append(temp)
            else:
                return render_template('create.html', error=f"No user found with name '{user}'")

        if len(UID) < 2:
            return render_template('create.html', error="alteast 2 users needed")

        start = start.replace('T', ' ') + ':00'
        end = end.replace('T', ' ') + ':00'
        # for id in UID:
        #     with conn:
        #         c.execute(
        #             f'select start, end from interviews where id in (SELECT interviewid FROM interuser where userid = {id})')
        #         times = c.fetchall()
        #     if not compatible((start, end), times):
        #         with conn:
        #             c.execute(f'Select name from users where id = {id}')
        #         return render_template('create.html', error=f"user '{c.fetchone()[0]}' is not available in given schedule")

        with conn:
            c.execute(
                f'INSERT INTO interviews(name, start, end) values("{name}", "{start}","{end}");')
            c.execute(f'SELECT last_insert_rowid()')
            Iid = c.fetchone()[0]
            print(Iid, type(Iid))
            for id in UID:
                c.execute(
                    f'INSERT INTO interuser values({Iid}, {id});')

        return render_template('create.html', success=True)
    else:
        return render_template('create.html')


@app.route('/edit-interview/<int:interviewid>')
def editInterview(interviewid):

    return render_template('edit.html')


if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
