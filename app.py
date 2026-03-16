from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "smart_secret_key"


# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        language = request.form['language']

        conn = sqlite3.connect('apps.db')
        cursor = conn.cursor()

        cursor.execute(
        "INSERT INTO users (email,password,language) VALUES (?,?,?)",
        (email,password,language)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('apps.db')
        cursor = conn.cursor()

        cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email,password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = user[1]      # email
            session['language'] = user[3]  # language

            return redirect(url_for('index'))

        else:
            return "Invalid Credentials"

    return render_template('login.html')


# ---------------- SEARCH PAGE ----------------
@app.route('/', methods=['GET','POST'])
def index():

    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        app_name = request.form['search'].lower()
        language = session['language']

        conn = sqlite3.connect('apps.db')
        cursor = conn.cursor()

        cursor.execute(
        "SELECT video_link FROM apps WHERE app_name=? AND language=?",
        (app_name,language)
        )

        result = cursor.fetchone()
        conn.close()

        if result:
            video = result[0]
        else:
            video = None

        return render_template(
            "result.html",
            video=video,
            name=app_name,
            language=language
        )

    return render_template("index.html")

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():

    session.pop('user', None)
    session.pop('language', None)

    return redirect(url_for('login'))
#-----------adminpage------------------------
@app.route('/admin', methods=['GET','POST'])
def admin():

    if request.method == 'POST':

        app_name = request.form['app_name']
        language = request.form['language']
        video = request.form['video']

        conn = sqlite3.connect('apps.db')
        cursor = conn.cursor()

        cursor.execute(
        "INSERT INTO apps (app_name, language, video_link) VALUES (?,?,?)",
        (app_name, language, video)
        )

        conn.commit()
        conn.close()

        return "App Tutorial Added Successfully!"

    return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True)