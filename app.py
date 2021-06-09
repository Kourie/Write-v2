from flask import Flask, render_template, g, request, redirect, flash, session, url_for
import sqlite3
import os
app = Flask(__name__)

DATABASE = 'time.db'

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    if 'username' in session:
        results = f'Logged in as {session["username"]}'
        return render_template("home.html", result=results)
    results = ("Not logged in")
    return render_template("home.html", result=results)

    

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register', methods=["GET","Post"])
def register_function():
    if request.method == "POST":
        cursor = get_db().cursor()
        user_ID = request.form.get("username")
        Email = request.form.get("Email")
        password = request.form.get("password")
        sql = ("INSERT INTO Account(user_ID,mail,password) VALUES (?,?,?)")
        print (user_ID)
        print (Email) 
        print (password)

        cursor.execute(sql,(user_ID,Email,password))
        get_db().commit()
        return redirect ("/login")


    return render_template("register.html")


@app.route('/logged')
def logged():
    home()
    cursor = get_db().cursor()
    sql = ("SELECT * FROM Account WHERE user_id = (?)")
    cursor.execute(sql,(session['username'],))
    result=cursor.fetchall()
    print (result)
    
    return render_template("logged.html", results=result)

@app.route('/fail')
def fail():
    return render_template("fail.html")



@app.route('/find', methods=["GET","Post"])  #broken fail safe, 
def login_function():
    if request.method == "POST":
       
        cursor = get_db().cursor()
        user_ID = request.form.get("username")
        password = request.form.get("password")
        find_user = ("SELECT * FROM Account WHERE (user_ID,password) = (?,?)")
        cursor.execute(find_user,(user_ID, password))
        results = cursor.fetchall()
        
        if len(results) > 0:
             #he have a user in the database with the right password
            session['username'] = request.form['username']
            return redirect ("/logged")
        
        else:
            flash ("error, check spelling and caps")
            return redirect ("/login")
            



@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)


