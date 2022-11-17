from flask import Flask, render_template, json, request, redirect
import database.db_connector as db
import os

app = Flask(__name__)
db_connection = db.connect_to_database()

app.config['MYSQL_CURSORCLASS'] = "DictCursor"

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/airports", methods=["POST", "GET"])
def airports():

    # insert into the airports entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Airport"):
            # grab user form inputs
            airportID = request.form["AirportID"]
            name = request.form["Name"]
            city = request.form["City"]
            state = request.form["State"]
        
            # assuming no null inputs
            query = "INSERT INTO Airports (AirportID, Name, City, State) VALUES (%s, %s,%s,%s);"
            # cur = db.connection.cursor()
            # cur.execute(query, (airportID, name, city, state))
            # db.connection.commit()
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(airportID, name, city, state))
            results = cursor.fetchall()

            return redirect("/airports")

    # Grab Airports data so we send it to our template to display
    if request.method == "GET":
        # db query to grab all the people in bsg_people
        query = "SELECT * FROM Airports;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("airports.html", data=data)

@app.route("/delete-airport/<string:id>")
def delete_airport(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Airports WHERE AirportID = '%s';" % (id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    data = cursor.fetchall()

    # redirect back to airport page
    return redirect("/airports")

@app.route("/edit-airport/<string:id>", methods=["POST", "GET"])
def edit_airport(id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Airports WHERE AirportID = '%s';" % (id)
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        return render_template("edit_airport.html", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        if request.form.get("Edit_Airport"):
            # grab user form inputs
            name = request.form["Name"]
            city = request.form["City"]
            state = request.form["State"]
            
            # . UPDATE table_name SET column1 = value1, column2 = value2 WHERE id=100;
            query = "UPDATE Airports SET Airports.Name = %s, Airports.City = %s, Airports.State = %s WHERE Airports.AirportID = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(name, city, state, id))
            data = cursor.fetchall()
            print(data)
            # redirect back to people page after we execute the update query
            return redirect("/airports")

# Airplanes
@app.route('/airplanes')
def airplanes():
    return render_template('airplanes.html')

# Flights
@app.route("/flights", methods=["POST", "GET"])
def flights():

    # insert into the flights entity
    if request.method == "POST":
        # fire off if user presses the Add Flight button
        if request.form.get("Add_Flight"):
            # grab user form inputs
            Origin = request.form["Origin"]
            Destination = request.form["Destination"]
            Departure = request.form["Departure"]
            Arrival = request.form["Arrival"]
            FlightDuration = request.form["FlightDuration"]
            Pilot = request.form["Pilot"]
            Copilot = request.form["Copilot"]
            Aircraft = request.form["Aircraft"]
            # Customers = request.form["Customers"]
        
            # assuming no null inputs
            query = "INSERT INTO Flights \
                (Origin, Destination, Departure, Arrival, FlightDuration, Pilot, Copilot, Aircraft) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor = db.execute_query(
                db_connection=db_connection, 
                query=query, 
                query_params=(Origin, Destination, Departure, Arrival, FlightDuration, Pilot, Copilot, Aircraft)
                )
            results = cursor.fetchall()
            return redirect("/flights")

    # Grab Flights data so we send it to our template to display
    if request.method == "GET":
        # db query to grab all the people in bsg_people
        # query = "SELECT \
        #     Origin, Destination, Arrival, FlightDuration, Pilot, Copilot, Aircraft, \
        #     Customers.FirstName AS FName, Customers.LastName AS LName \
        #     FROM Flights \
        #     INNER JOIN Flights_has_Customers \
        #     ON Flights.FlightID = Flights_has_Customers.FlightID;"
        query = "SELECT \
            FlightID, Origin, Destination, Departure, Arrival, FlightDuration, Pilot, Copilot, Aircraft, \
            Customers.FirstName AS fname, Customers.LastName AS lname   \
            FROM Flights \
            INNER JOIN Flights_has_Customers \
            ON Flights.FlightID = Flights_has_Customers.Flights_FlightID \
            LEFT JOIN Customers \
            ON Flights_has_Customers.Customers_CustomerID = Customers.CustomerID;"

        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        # query to grab info from Customers
        query2 = "SELECT FirstName, LastName FROM Customers"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        customers_data = cursor.fetchall()

        # query to grab info from Flights_has_Customers intersection table
        query3 = "SELECT * FROM Flights_has_Customers"
        cursor = db.execute_query(db_connection=db_connection, query=query3)
        fhc_data = cursor.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("flights.html", data=data, customers=customers_data, fhc=fhc_data)


# route for delete functionality, deleting an airport
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete-flight/<int:id>")
def delete_flight(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Flights WHERE FlightID = '%s';" % (id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    data = cursor.fetchall()

    # redirect back to airport page
    return redirect("/flights")


# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit-flight/<int:id>", methods=["POST", "GET"])
def edit_flight(id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Flights WHERE FlightID = '%s';" % (id)
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        return render_template("edit_flight.html", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        if request.form.get("Edit_Flight"):
            # grab user form inputs
            name = request.form[""]
            city = request.form[""]
            state = request.form[""]
        
            query = "UPDATE Flights SET Airports.Name = %s, Airports.City = %s, Airports.State = %s WHERE Airports.AirportID = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(name, city, state, id))
            data = cursor.fetchall()
            print(data)
            # redirect back to people page after we execute the update query
            return redirect("/flights")

# Pilots
@app.route('/pilots')
def pilots():
    return render_template('pilots.html')

# Customers
@app.route('/customers')
def customers():
    return render_template('customers.html')

# Flights_has_customers
@app.route('/flights-customers')
def flightsCustomers():
    return render_template('flights_has_customers.html')


# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    port = int(os.environ.get('PORT', 8251))
    app.run(port=port, debug=True)