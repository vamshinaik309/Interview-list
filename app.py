from flask import Flask, render_template, url_for, request, redirect
import sqlite3
from datetime import datetime
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


def compatible(X, L):
    def f(x): return datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    S = f(X[0])
    E = f(X[1])
    for (s, e) in L:
        s = f(e)
        e = f(e)
        if not (E <= s or e <= S):
            return False
    return True


def getUsers(ID):
    c.execute(
        f'SELECT name from users where id in (SELECT userid from interuser where interviewid={ID});')
    st = []
    for x in c.fetchall():
        st.append(x[0])
    return st


@app.route('/')
@app.route('/interviews-list')
def home():
    params = {}
    c.execute('SELECT name from users;')
    params['users'] = [x[0] for x in c.fetchall()]

    c.execute('SELECT * from interviews;')
    interviews = [{'id': x[0],
                   'name': x[1],
                   'users': getUsers(x[0]),
                   'start': x[2],
                   'end': x[3]} for x in c.fetchall()]

    params['interviews'] = interviews
    return render_template('list.html', **params)
    # return render_template('list.html', interviews=interviews)


@app.route('/create-interview', methods=['POST', 'GET'])
def createInterview():
    params = {}
    c.execute('SELECT name from users;')
    params['users'] = [x[0] for x in c.fetchall()]

    if request.method == 'POST':
        name = request.form['name'].strip()
        users = request.form['users'].strip().split(';')
        start = request.form['start'].strip()
        end = request.form['end'].strip()
        if '' in [name, users, start, end]:
            return render_template('create.html', error="All fields are required")

        UID = []
        users = list(dict.fromkeys([user.strip() for user in users]))
        for user in users:
            with conn:
                c.execute(f'SELECT id from users where name="{user}";')
            temp = c.fetchone()
            if temp is not None:
                temp = temp[0]
                UID.append(temp)
            else:
                params['error'] = f"No user found with name '{user}'"
                return render_template('create.html', **params)

        if len(UID) < 2:
            params['error'] = "alteast 2 users needed"
            return render_template('create.html', **params)

        start = start.replace('T', ' ') + ':00'
        end = end.replace('T', ' ') + ':00'
        for id in UID:
            with conn:
                c.execute(
                    f'select start, end from interviews where id in (SELECT interviewid FROM interuser where userid = {id})')
                times = c.fetchall()
            if not compatible((start, end), times):
                with conn:
                    c.execute(f'Select name from users where id = {id}')

                params['error'] = f"user '{c.fetchone()[0]}' is not available in given schedule"
                return render_template('create.html', **params)

        with conn:
            c.execute(
                f'INSERT INTO interviews(name, start, end) values("{name}", "{start}","{end}");')
            c.execute(f'SELECT last_insert_rowid()')
            Iid = c.fetchone()[0]
            for id in UID:
                c.execute(
                    f'INSERT INTO interuser values({Iid}, {id});')
        params['success'] = True
        return render_template('create.html', **params)
    else:
        return render_template('create.html', **params)


@app.route('/edit-interview/<int:interviewid>', methods=['POST', 'GET'])
def editInterview(interviewid):
    with conn:
        c.execute(f'select * from interviews where id = {interviewid}')
        x = c.fetchone()

    params = {}
    c.execute('SELECT name from users;')
    params['users'] = [x[0] for x in c.fetchall()]
    params['editform'] = True
    params['fillformvalue'] = {
        'id': interviewid,
        'name': x[1],
        'users': '; '.join(getUsers(interviewid)),
        'start': x[2].replace(' ', 'T')[:-3],
        'end': x[3].replace(' ', 'T')[:-3]
    }

    if request.method == 'POST':
        name = request.form['name'].strip()
        users = request.form['users'].strip().split(';')
        start = request.form['start'].strip()
        end = request.form['end'].strip()
        if '' in [name, users, start, end]:
            return render_template('create.html', error="All fields are required")

        UID = []
        users = list(dict.fromkeys([user.strip() for user in users]))
        for user in users:
            with conn:
                c.execute(f'SELECT id from users where name="{user}";')
            temp = c.fetchone()
            if temp is not None:
                temp = temp[0]
                UID.append(temp)
            else:
                params['error'] = f"No user found with name '{user}'"
                return render_template('create.html', **params)

        if len(UID) < 2:
            params['error'] = "alteast 2 users needed"
            return render_template('create.html', **params)

        start = start.replace('T', ' ') + ':00'
        end = end.replace('T', ' ') + ':00'
        for id in UID:
            with conn:
                c.execute(
                    f'select start, end from interviews where id in (SELECT interviewid FROM interuser where userid = {id}) and id !={interviewid}')
                times = c.fetchall()
            if not compatible((start, end), times):
                with conn:
                    c.execute(f'Select name from users where id = {id}')

                params['error'] = f"user '{c.fetchone()[0]}' is not available in given schedule"
                return render_template('create.html', **params)

        with conn:
            c.execute(
                f'update interviews set name = "{name}",start="{start}", end="{end}" where id = {interviewid}')
            c.execute(
                f'select userid from interuser where interviewid={interviewid}')
            oldUID = [x[0] for x in c.fetchall()]
            for id in set(oldUID)-set(UID):
                c.execute(
                    f'DELETE FROM interuser where interviewid={interviewid} and userid={id};')

            for id in set(UID)-set(oldUID):
                c.execute(
                    f'INSERT INTO interuser values({interviewid}, {id});')

        return redirect(url_for('home'))
    else:
        return render_template('create.html', **params)


if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
