from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "bagus-adi"

DB_HOST = "localhost"
DB_NAME = "db_flaskmyproject"
DB_USER = "postgres"
DB_PASS = "postgres"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/')
def index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM students"
    cur.execute(s)
    list_users = cur.fetchall()
    email = session.get('email', '')
    return render_template('index.html', list_users=list_users, email=email)

@app.route('/add_student', methods=['POST'])
def add_student():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
    if not fname or not email:
        flash('Semua input harus diisi!')
        session['email'] = email
        return redirect(url_for('index'))
    else:
        cur.execute("INSERT INTO students (fname, lname, email) VALUES (%s,%s,%s)", (fname, lname, email))
        conn.commit()
        flash('Student Added Successfully')
        session.pop('nama', None)
        session.pop('email', None)
        return redirect(url_for('index'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('SELECT * FROM students WHERE id = {0}'.format (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', student=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_student(id):
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']

        if not fname or not email:
            flash('Semua input harus diisi!')
            session['email'] = email
            return redirect(url_for('index'))
        else:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""
                        UPDATE students
                        SET fname = %s,
                            lname = %s,
                            email = %s
                        WHERE id = %s
                    """, (fname, lname, email, id))
            flash('Student Updated Successfully')
            conn.commit()
            return redirect(url_for('index'))


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_student(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('DELETE FROM students WHERE id = {0}'.format(id))
    conn.commit()
    flash('Student Removed Successfully')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
