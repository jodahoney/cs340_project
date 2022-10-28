from flask import Flask, render_template

app = Flask(__name__)

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