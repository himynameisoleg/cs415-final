from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import re

app = Flask(__name__)

app.secret_key = 'secret'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'movies'
# Extra configs, optional:
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
# app.config["MYSQL_CUSTOM_OPTIONS"] = {"ssl": {"ca": "/path/to/ca-file"}}  # https://mysqlclient.readthedocs.io/user_guide.html#functions-and-attributes


# Intialize MySQL
mysql = MySQL(app)

@app.route('/index.html')
def index():
    if session.get('loggedin'):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Movies ORDER BY IMDB_Rating DESC LIMIT 12')
        movies = cursor.fetchall()

        return render_template('index.html', movies=movies, the_title='Welcome')
    else:
        return redirect(url_for('login'))

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT * FROM Users WHERE UserID = %s AND Password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['UserID']
            session['username'] = account['UserID']
            session['age'] = account['Age']
            session['city'] = account['City']
            # Redirect to home page
            msg = 'Logged in successfully!'
            return redirect(url_for('index'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Maybe try "admin" and "password"?'

    return render_template('login.html', msg=msg, the_title='Welcome')
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/signup', methods =['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'age' in request.form and 'city' in request.form:
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        city = request.form['city']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Users WHERE UserID = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[0-9]+', age):
            msg = 'Invalid Age !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[A-Za-z]+', city):
            msg = 'City must contain only characters!'
        elif not username or not password or not age or not city:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO Users VALUES (% s, % s, % s, % s)', (username, password, age, city, ))
            mysql.connection.commit()

            session['loggedin'] = True
            session['id'] = username
            session['username'] = username
            session['age'] = age
            session['city'] = city

            msg = 'You have successfully registered !'
            return redirect(url_for('index')) 
            
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg = msg, the_title='Sign Up')

@app.route('/about')
def about():
    return render_template('about.html', the_title='About')

@app.route('/search')
def search():
    return render_template('search.html', the_title='Search')

@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html', the_title='Recommendations')

@app.route('/results')
def results():
    return render_template('results.html', the_title='Search Results')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
