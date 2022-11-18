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

    #TODO: 
    # - Add search feature to Flights page
    # - Add checkbox to the flights page to add multiple customers
    # - Make sure it is possible that a flight can be added without customers
    #   - but that is the ONLY nullable option
    # - add in the filter functionality to flights w/ customers so you can search for
    #  that specific customer list based on click from flights or search in base page
    # - add pilot name and copilot name to results table intead of id\

    # insert into the flights entity
    if request.method == "POST":
        # fire off if user presses the Add Flight button
        if request.form.get("Add_Flight"):
            # grab user form inputs
            Origin = request.form["origin-select"]
            Destination = request.form["destination-select"]
            Departure = request.form["Departure"]
            Arrival = request.form["Arrival"]
            FlightDuration = request.form["FlightDuration"]
            Pilot = request.form["pilot-select"]
            CoPilot = request.form["copilot-select"]
            Aircraft = request.form["aircraft-select"]
            Customers = request.form.getlist("customer-select")
        
            # assuming no null inputs
            query = "INSERT INTO Flights \
                (Origin, Destination, Departure, Arrival, FlightDuration, Pilot, CoPilot, Aircraft) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
                RETURNING FlightID;"
            cursor = db.execute_query(
                db_connection=db_connection, 
                query=query, 
                query_params=(Origin, Destination, Departure, Arrival, FlightDuration, Pilot, CoPilot, Aircraft)
                )
            results = cursor.fetchall()
            flightid = results[0]['FlightID']
            print(Customers)

            # If they provided customers to book, add them to the flight
            if Customers:
                for customerid in Customers:
                    # Add to flights_has_customers table
                    query = "INSERT INTO Flights_has_Customers \
                        (Flights_FlightID, Customers_CustomerID) \
                        VALUES (%s, %s);"
                    cursor = db.execute_query(
                        db_connection=db_connection,
                        query=query,
                        query_params=(flightid, customerid)
                    )
            return redirect("/flights")

    # Grab Flights data so we send it to our template to display
    if request.method == "GET":
        # OLD WAY OF SELECTING CUSTOMERS INTO TABLE:
        # query = "SELECT \
        #     FlightID, Origin, Destination, Departure, Arrival, FlightDuration, Pilot, Copilot, Aircraft, \
        #     Customers.FirstName AS fname, Customers.LastName AS lname   \
        #     FROM Flights \
        #     INNER JOIN Flights_has_Customers \
        #     ON Flights.FlightID = Flights_has_Customers.Flights_FlightID \
        #     LEFT JOIN Customers \
        #     ON Flights_has_Customers.Customers_CustomerID = Customers.CustomerID;"

        query = "SELECT * FROM Flights;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        query2 = "SELECT CustomerID, FirstName, LastName FROM Customers;"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        customer_data = cursor.fetchall()

        query3 = "SELECT AirportID, Name FROM Airports;"
        cursor = db.execute_query(db_connection=db_connection, query=query3)
        airport_data = cursor.fetchall()

        query4 = "SELECT PilotID, FirstName, LastName FROM Pilots;"
        cursor = db.execute_query(db_connection=db_connection, query=query4)
        pilot_data = cursor.fetchall()

        query5 = "Select TailNumber, Make, Model FROM Airplanes;"
        cursor = db.execute_query(db_connection=db_connection, query=query5)
        aircraft_data = cursor.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("flights.html", 
            data=data, 
            customer_data=customer_data, 
            airport_data=airport_data,
            pilot_data=pilot_data,
            aircraft_data=aircraft_data)


# route for delete functionality, deleting a flight
@app.route("/delete-flight/<int:id>")
def delete_flight(id):

    # delete the flight from the flights table
    query = "DELETE FROM Flights WHERE FlightID = '%s';" % (id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    
    # remove all flight-customer relationships from intersection
    query2 = "DELETE FROM Flights_has_Customers \
        WHERE Flights_FlightID = '%s';" % (id)
    cursor = db.execute_query(db_connection=db_connection, query=query2)

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
@app.route('/flights-customers', methods=["POST", "GET"])
def flightsCustomers():
    if request.method == "GET":
        query = "SELECT * FROM Flights_has_Customers;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        query2 = "SELECT Customers_CustomerID, \
            Customers.FirstName AS fname, Customers.LastName AS lname \
            FROM Flights_has_Customers \
            INNER JOIN Customers \
            ON Flights_has_Customers.Customers_CustomerID = Customers.CustomerID  \
            ;"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        customer_data = cursor.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("flights_has_customers.html", data=data, customer_data=customer_data)
    
    return render_template('flights_has_customers.html')

# TODO:
@app.route('/flights-customers/<int:id>', methods=["POST", "GET"])
def indFlightsCustomers():
    return render_template('ind_flights_has_customers.html')

# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    port = int(os.environ.get('PORT', 8251))
    app.run(port=port, debug=True)