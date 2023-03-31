from flask import Flask, render_template
from flask import jsonify
import socket 

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', the_title='Movies Database')

@app.route('/signup.html')
def signup():
    return render_template('signup.html', the_title='Sign Up')

@app.route('/loginpage.html')
def loginpage():
    return render_template('loginpage.html', the_title='Log In')

@app.route('/about.html')
def about():
    return render_template('about.html', the_title='About')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html', the_title='Dashboard')

@app.route('/results.html')
def results():
    return render_template('results.html', the_title='Search Results')

@app.route('/ip')
def ip():
    hostname = socket.gethostname()    
    IPAddr = socket.gethostbyname(hostname)
    d = {
        "hostname": hostname,
        "IPAddr": IPAddr,
    }   
    return jsonify(d)

@app.route('/mysql')
def test_db_connection():
    try:
        from mysql.connector import connect
        cnx = connect(
            host='127.0.0.1',
            database='movies',
            user='root',
            password='root', 
            port=3306
        )
        d = {
            "success": True,
            "message": "Connected to database successfully",
        }
    except Exception as e:
        d = {
            "success": False,
            "message": str(e),
        }
    return jsonify(d)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
