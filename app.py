import datetime
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

# Routes
@app.route('/')
@app.route('/index')
def index():
    if session.get('loggedin'):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Movies ORDER BY IMDB_Rating DESC LIMIT 9')
        movies = cursor.fetchall()

        return render_template('index.html', movies=movies, the_title='Welcome')
    else:
        return redirect(url_for('signup'))

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
            now = datetime.datetime.now()

            session['loggedin'] = True
            session['id'] = account['UserID']
            session['username'] = account['UserID']
            session['age'] = account['Age']
            session['city'] = account['City']
            session['logged_in_at'] = now.strftime("%c")
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

@app.route('/search', methods=['GET', 'POST'])
def search():
    msg = ''

    # get list of genres
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT DISTINCT Genre FROM Movies ORDER BY Genre ASC')
    genres = cursor.fetchall()

    # process request by input type
    if request.method == 'POST' and 'search-title' in request.form:
        title = request.form['search-title']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Movies WHERE Title LIKE % s', ('%' + title + '%', ))
        movies = cursor.fetchall()

        if not movies:
            msg = 'No movies found!'

        return render_template('search.html', msg=msg, genres=genres, movies=movies)
    
    elif request.method == 'POST' and 'search-actor' in request.form:
        actor = request.form['search-actor']

        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT * FROM Movies WHERE Star1 LIKE % s 
                        OR Star2 LIKE % s OR Star3 LIKE % s OR Star4 LIKE % s """, ('%' + actor + '%', '%' + actor + '%', '%' + actor + '%', '%' + actor + '%', ))
        movies = cursor.fetchall()

        if not movies:
            msg = 'No movies found!'

        return render_template('search.html', msg=msg, genres=genres, movies=movies)

    elif request.method == 'POST' and 'search-genre' in request.form:
        genre = request.form['search-genre']

        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT * FROM Movies WHERE Genre LIKE % s LIMIT 100""", ('%' + genre + '%', ))
        movies = cursor.fetchall()

        if not movies:
            msg = 'No movies found!'

        return render_template('search.html', msg=msg, genres=genres, movies=movies)
    
    elif request.method == 'POST' and 'search-director' in request.form:
        director = request.form['search-director']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Movies WHERE Director LIKE % s', ('%' + director + '%', ))
        movies = cursor.fetchall()

        if not movies:
            msg = 'No movies found!'

        return render_template('search.html', msg=msg, genres=genres, movies=movies)
    
    else:

        return render_template('search.html', msg=msg, genres=genres, the_title='Search')

@app.route('/favorite', methods=['GET', 'POST'])
def favorite():
    
    msg=''
    if request.method == 'POST' and 'favorite-add' in request.form:
        title = request.form['favorite-add']
        username = session['username']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Favorites WHERE UserID = % s AND Title = % s', (username, title, ))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute('INSERT INTO Favorites VALUES (% s, % s, CURDATE())', (username, title, ))
            mysql.connection.commit()
            msg = 'Added to favorites!'
        else:
            msg = 'You already favorited this movie!'

        return render_template('search.html', msg=msg)
    elif request.method == 'POST' and 'favorite-remove' in request.form:
        title = request.form['favorite-remove']
        username = session['username']

        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Favorites WHERE UserID = % s AND Title = % s', (username, title, ))
        mysql.connection.commit()

        msg = 'Removed from favorites!'
        return render_template('profile.html', msg=msg)
    else:
        return redirect('search.html', msg=msg)

@app.route('/recommendations')
def recommendations():
    if session.get('loggedin'):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT m.Title, m.Poster_Link, m.Released_Year, m.IMDB_Rating, m.Runtime, m.Certificate, m.Director, m.Star1, m.Star2, m.Star3, m.Star4, COUNT(f.Title) AS Count
            FROM Movies AS m
            JOIN Favorites AS f ON f.Title = m.Title
            JOIN Users AS u ON f.UserID = u.UserID
            WHERE u.City = % s
            GROUP By f.Title
            ORDER BY COUNT(f.Title) DESC
            LIMIT 5;
        """, (session['city'], ))
        top_your_city = cursor.fetchall()


        upper_age = int(session['age']) + 5
        lower_age = int(session['age']) - 5
        cursor.execute("""
            SELECT m.Title, m.Poster_Link, m.Released_Year, m.IMDB_Rating, m.Runtime, m.Certificate, m.Director, m.Star1, m.Star2, m.Star3, m.Star4, COUNT(f.Title) AS Count
            FROM Movies AS m
            JOIN Favorites AS f ON f.Title = m.Title
            JOIN Users AS u ON u.UserID = f.UserID
            WHERE u.Age BETWEEN % s AND % s
            GROUP BY f.Title
            ORDER BY COUNT(f.Title) DESC
            LIMIT 5
        """, (lower_age, upper_age, ))
        top_age = cursor.fetchall()

        cursor.execute("""
            SELECT Genre
            FROM Movies
            GROUP BY Genre
            ORDER BY COUNT(Genre) DESC
            LIMIT 25  
        """)
        top_genre = cursor.fetchall()
      
        cursor.execute("""
            SELECT m.Title, m.Poster_Link, m.Released_Year, m.IMDB_Rating, m.Runtime, m.Certificate, m.Director, m.Gross
            FROM Movies AS m
            GROUP BY m.Title
            ORDER BY MAX(m.Gross) DESC
            LIMIT 10
        """)
        top_grossing = cursor.fetchall()

        cursor.execute("""
            SELECT a.Name, COUNT(a.Name) AS Favorited FROM Actors AS a
            JOIN Favorites AS f ON f.Title = a.Title
            WHERE a.Name IN (SELECT m.Star1 FROM Movies AS m JOIN Favorites AS f ON f.Title = m.Title) 
            OR a.Name IN (SELECT m.Star2 FROM Movies AS m JOIN Favorites AS f ON f.Title = m.Title)
            OR a.Name IN (SELECT m.Star3 FROM Movies AS m JOIN Favorites AS f ON f.Title = m.Title)
            OR a.Name IN (SELECT m.Star4 FROM Movies AS m JOIN Favorites AS f ON f.Title = m.Title)
            GROUP BY a.Name
            ORDER BY COUNT(a.Name) DESC
            LIMIT 25
        """)
        top_actors = cursor.fetchall()

        cursor.execute("""
            SELECT f.Title, u.City, COUNT(*) AS Count FROM Favorites AS f
            JOIN Users AS u ON f.UserID = u.UserID
            GROUP BY f.Title, u.City
            ORDER BY Count DESC 
            LIMIT 5
        """)
        top_by_city = cursor.fetchall()

        return render_template('recommendations.html', top_your_city=top_your_city, top_age=top_age, top_genre=top_genre, top_grossing=top_grossing, top_actors=top_actors, top_by_city=top_by_city)
    else:
        return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if session.get('loggedin'):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT f.Title, f.Date_Added FROM Favorites AS f 
            JOIN Users AS u ON u.UserID = f.UserID
            WHERE f.UserID = % s
        """, (session['username'], ))
        movies = cursor.fetchall()

        return render_template('profile.html', movies=movies)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
