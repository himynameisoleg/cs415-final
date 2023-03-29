from flask import Flask, render_template
from flask import jsonify
import socket 

app = Flask(__name__)

# two decorators, same function
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', the_title='Tiger Home Page')

@app.route('/symbol.html')
def symbol():
    return render_template('symbol.html', the_title='Tiger As Symbol')

@app.route('/myth.html')
def myth():
    return render_template('myth.html', the_title='Tiger in Myth and Legend')

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
        # google sql cloud database -- ip whitelisting test for heroku app
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
    app.run(debug=True)
