from flask import Flask, render_template, request, json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_dehoneyj'
app.config['MYSQL_PASSWORD'] = '2584' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_dehoneyj'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return 'Hello, World'

# Airports
@app.route('/airports')
def airports():
    return render_template('airports.html')

# Airplanes
@app.route('/airplanes')
def airplanes():
    return render_template('airplanes.html')

# Flights
@app.route('/flights')
def flights():
    return render_template('flights.html')

# Pilots
@app.route('/pilots')
def pilots():
    return render_template('pilots.html')

# Customers
@app.route('/customers')
def customers():
    return render_template('customers.html')


# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=8251, debug=True)