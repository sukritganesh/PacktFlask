from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3

app = Flask(__name__)

# CONFIGURATION
# https://flask.palletsprojects.com/en/2.0.x/config/
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisasecret!'

def connect_db():
    sql = sqlite3.connect('C:/sqlite/data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# ROUTES

@app.route('/')
def index():
    session.pop('name', None)
    return '<h1>Hello World!</h1>'

@app.route('/home', methods=['GET', 'POST'], defaults={'name':'Default'})
@app.route('/home/<name>', methods=['GET', 'POST'])
def home(name):
    session['name'] = name
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()

    return render_template('home.html', name=name, display=True, \
        myList=['one', 'two', 'three'], listOfDicts=[{'name' : 'Zach'}, {'name' : 'Zoe'}], results=results)

@app.route('/json')
def json():
    if 'name' in session:
        mylist = [1,2,3,4]
        name = session['name']
    else:
        name = 'NotInSession!'
    return jsonify({'key' : 'value', 'key2' : [1,2,3], 'key3' : {'a' : 1, 'b' : 2, 'c' : 3}, 'name' : name})

@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()
    name = data['name']
    location = data['location']
    randomlist = data['randomlist']
    return jsonify({'result' : 'Success!', 'name' : name, 'location' : location, 'randomkeyinlist' : randomlist[1]})

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>Hi {}. You are from {}. You are on the query page!</h1>'.format(name, location)

@app.route('/theform', methods=['GET', 'POST'])
def theform():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']

        db = get_db()
        db.execute('insert into users (name, location) values (?, ?)', [name, location])
        db.commit()

        # return '<h1>Hello {}. You are from {}. You have submitted the form successfully!</h1>'.format(name, location)
        return redirect(url_for('home', name=name, location=location))

# @app.route('/theform', methods=['GET'])
# def theform():
#     return '''<form method="POST" action="/theform">
#         <input type="text" name="name">
#         <input type="text" name="location">
#         <input type="submit" value="Submit">
#     </form>'''

# @app.route('/theform', methods=['POST'])
# def processform():
#     name = request.form['name']
#     location = request.form['location']
#     return '<h1>Hello {}. You are from {}. You have submitted the form successfully!</h1>'.format(name, location)

@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return '<h1>The ID is {}. The name is {}. The location is {}.</h1>'.format(results[1]['id'], results[1]['name'], results[1]['location'])

if __name__ == '__main__':
    app.run(debug=True)

