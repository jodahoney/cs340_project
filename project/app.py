from flask import Flask, render_template, json, request, redirect
import database.db_connector as db
import datetime
import os

app = Flask(__name__)
db_connection = db.connect_to_database()

app.config['MYSQL_CURSORCLASS'] = "DictCursor"

"""
TODO:
- flights has customers create, update, delete
- make sure that all of the update forms have the pre filled in information 
    as the value for text fields (like in flights)
- add a search / filter
    - needs to also have the ability to search using text or filter using a dynamically populated list of 
        properties.
- code citations
    - In the code, you have to mention 1. the full details of the citation scope (e.g. module, function or line), 
        2. if the code is copied, adapted, or based, and 3. the source (URL). I don't think it's required in the README, 
        but it's probably best to mention the node starter app and any sources you used. 
- Note that the nullable foreign key that we have is that you can create a flight without customers.
- In a one-to-many relationship, you should be able to set the foreign key value to NULL using UPDATE, 
    that removes the relationship. In case none of the one-to-many relationships in your database has 
    partial participation, you would need to change that to make sure they can have NULL values.
- In a many-to-many relationship, one should be able to delete a row from the intersection table without creating
     a data anomaly in the related tables. If you implement DELETE functionality on at least ( 1 ) many - 
     to - many relationship table , such that the rows in the relevant entity tables are not impacted , 
     that is sufficient.
- To continue the example from above, if you have 5 tables in your schema, then at a minimum, we expect you to 
    implement 5 SELECTs, 5 INSERTs, 2 UPDATEs (M:M 1 NULLable relationship), 1 DELETE (M:M), and 1 Search/Dynamic 
    for a total of 14 functions. 
"""

def calculate_flight_time(arrival, departure):
    """
    Accepts the string output by the HTML datetime-local input form and converts
    to a time delta in number of minutes from departure to arrival.
    """
    arrival_datetime = datetime.datetime.strptime(arrival,"%Y-%m-%dT%H:%M")
    departure_datetime = datetime.datetime.strptime(departure,"%Y-%m-%dT%H:%M")

    time_delta = arrival_datetime - departure_datetime
    FlightDuration = (time_delta.days * 24) + (time_delta.seconds // 60)
    
    return FlightDuration


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/airports", methods=["POST", "GET"])
def airports():

    # insert into the airports entity
    if request.method == "POST":
        
        if request.form.get("Add_Airport"):
            # grab user form inputs
            airportID = request.form["AirportID"]
            name = request.form["Name"]
            city = request.form["City"]
            state = request.form["State"]
        
            # assuming no null inputs
            query = "INSERT INTO Airports (`AirportID`, `Name`, `City`, `State`) VALUES (%s, %s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(airportID, name, city, state))
            results = cursor.fetchall()

            return redirect("/airports")

    # Grab Airports data so we send it to our template to display
    if request.method == "GET":
        query = "SELECT * FROM Airports;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        return render_template("airports.html", data=data)


@app.route("/delete-airport/<string:id>")
def delete_airport(id):
    query = "DELETE FROM Airports WHERE AirportID = '%s';" % (id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    data = cursor.fetchall()

    # redirect back to airport page
    return redirect("/airports")


@app.route("/edit-airport/<string:id>", methods=["POST", "GET"])
def edit_airport(id):
    if request.method == "GET":
        query = "SELECT * FROM Airports WHERE AirportID = '%s';" % (id)
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        return render_template("edit_airport.html", data=data)

    if request.method == "POST":
        if request.form.get("Edit_Airport"):
            name = request.form["Name"]
            city = request.form["City"]
            state = request.form["State"]
            
            query = "UPDATE Airports SET Airports.Name = %s, Airports.City = %s, Airports.State = %s WHERE Airports.AirportID = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(name, city, state, id))
            data = cursor.fetchall()
            print(data)
            
            return redirect("/airports")


@app.route("/airplanes", methods=["POST", "GET"])
def airplanes():

    # insert into the airplanes entity
    if request.method == "POST":
        # fire off if user presses the Add airplane button
        if request.form.get("Add_Airplane"):
            # grab user form inputs
            tail_number = request.form["TailNumber"]
            make = request.form["Make"]
            model = request.form["Model"]
            air_range = request.form["Range"]
            fuel_capacity = request.form["FuelCapacity"]
            last_maintenance_performed = request.form["LastMaintenancePerformed"]
            maintenance_frequency = request.form["MaintenanceFrequency"]
        
            # assuming no null inputs
            query = "INSERT INTO Airplanes (`TailNumber`, `Make`, `Model`, `Range`, `FuelCapacity`, `LastMaintenancePerformed`, `MaintenanceFrequency`) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(tail_number, make, model, air_range, fuel_capacity, last_maintenance_performed, maintenance_frequency))
            results = cursor.fetchall()

            return redirect("/airplanes")

    # Grab Airplanes data so we send it to our template to display
    if request.method == "GET":
        query = "SELECT * FROM Airplanes;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        return render_template("airplanes.html", data=data)


@app.route("/delete-airplane/<string:id>")
def delete_airplane(id):
    query = "DELETE FROM Airplanes WHERE TailNumber = '%s';" % (id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    data = cursor.fetchall()

    # redirect back to airplanes page
    return redirect("/airplanes")


@app.route("/edit-airplane/<string:id>", methods=["POST", "GET"])
def edit_airplane(id):
    if request.method == "GET":
        query = "SELECT * FROM Airplanes WHERE TailNumber = '%s';" % (id)
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        return render_template("edit_airplane.html", data=data)

    if request.method == "POST":
        if request.form.get("Edit_Airplane"):
            make = request.form["Make"]
            model = request.form["Model"]
            range = request.form["Range"]
            fuel_capacity = request.form["FuelCapacity"]
            last_maintenance_performed = request.form["LastMaintenancePerformed"]
            maintenance_frequency = request.form["MaintenanceFrequency"]
           
            query = "UPDATE Airplanes SET Airplanes.Make = %s, Airplanes.Model = %s, Airplanes.Range = %s, Airplanes.FuelCapacity = %s, Airplanes.LastMaintenancePerformed = %s, Airplanes.MaintenanceFrequency = %s WHERE Airplanes.TailNumber = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(make, model, range, fuel_capacity, last_maintenance_performed, maintenance_frequency, id))
            data = cursor.fetchall()
            print(data)
 
            return redirect("/airplanes")


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
            Pilot = request.form["pilot-select"]
            CoPilot = request.form["copilot-select"]
            Aircraft = request.form["aircraft-select"]
            Customers = request.form.getlist("customer-select")

            
            # Calculate travel time
            FlightDuration = calculate_flight_time(Arrival, Departure)
        
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

    # Grab Flights and all related data so we send it to our template to display
    if request.method == "GET":

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

        return render_template("flights.html", 
            data=data, 
            customer_data=customer_data, 
            airport_data=airport_data,
            pilot_data=pilot_data,
            aircraft_data=aircraft_data
            )


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


@app.route("/edit-flight/<int:id>", methods=["POST", "GET"])
def edit_flight(id):
    if request.method == "GET":
        
        query = "SELECT * FROM Flights WHERE FlightID = '%s';" % (id)

        query3 = "SELECT AirportID, Name FROM Airports;"
        cursor = db.execute_query(db_connection=db_connection, query=query3)
        airport_data = cursor.fetchall()

        query4 = "SELECT PilotID, FirstName, LastName FROM Pilots;"
        cursor = db.execute_query(db_connection=db_connection, query=query4)
        pilot_data = cursor.fetchall()

        query5 = "Select TailNumber, Make, Model FROM Airplanes;"
        cursor = db.execute_query(db_connection=db_connection, query=query5)
        aircraft_data = cursor.fetchall()

        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        return render_template("edit_flight.html", 
            data=data, 
            # customer_data=customer_data, 
            airport_data=airport_data,
            pilot_data=pilot_data,
            aircraft_data=aircraft_data)

    if request.method == "POST":
        if request.form.get("Edit_Flight"):
            
            # grab user form inputs
            Origin = request.form["origin-select"]
            Destination = request.form["destination-select"]
            Departure = request.form["Departure"]
            Arrival = request.form["Arrival"]
            Pilot = request.form["pilot-select"]
            CoPilot = request.form["copilot-select"]
            Aircraft = request.form["aircraft-select"]

            FlightDuration = calculate_flight_time(Arrival, Departure)
        
            query = "UPDATE Flights SET Flights.Origin = %s, Flights.Destination = %s, Flights.Departure = %s, \
                Flights.Arrival = %s, Flights.FlightDuration = %s, Flights.Pilot = %s, Flights.CoPilot = %s, Flights.Aircraft = %s \
                WHERE Flights.FlightID = %s;"
            cursor = db.execute_query(db_connection=db_connection,
                query=query,
                query_params=(Origin, Destination, Departure, Arrival, FlightDuration, Pilot, CoPilot, Aircraft, id)
            )
            data = cursor.fetchall()

            return redirect("/flights")


@app.route("/pilots", methods=["POST", "GET"])
def pilots():

    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Pilot"):
            # grab user form inputs
            fname = request.form["FirstName"]
            lname = request.form["LastName"]
            phone_number = request.form["PhoneNumber"]
        
            # assuming no null inputs
            query = "INSERT INTO Pilots (`FirstName`, `LastName`, `PhoneNumber`) VALUES (%s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(fname, lname, phone_number))
            results = cursor.fetchall()

            return redirect("/pilots")

    if request.method == "GET":
        query = "SELECT * FROM Pilots;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        return render_template("pilots.html", data=data)


@app.route("/delete-pilot/<string:id>")
def delete_pilot(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Pilots WHERE PilotID = '%s';" % (id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    data = cursor.fetchall()

    return redirect("/pilots")


@app.route("/edit-pilot/<string:id>", methods=["POST", "GET"])
def edit_pilot(id):
    if request.method == "GET":
        query = "SELECT * FROM Pilots WHERE PilotID = '%s';" % (id)
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        return render_template("edit_pilot.html", data=data)

    if request.method == "POST":
        if request.form.get("Edit_Pilot"):
            # grab user form inputs
            fname = request.form["FirstName"]
            lname = request.form["LastName"]
            phone_number = request.form["PhoneNumber"]
            
            query = "UPDATE Pilots SET Pilots.FirstName = %s, Pilots.LastName = %s, Pilots.PhoneNumber = %s WHERE Pilots.PilotID = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(fname, lname, phone_number, id))
            data = cursor.fetchall()
            print(data)
            
            return redirect("/pilots")


@app.route("/customers", methods=["POST", "GET"])
def customers():

    # insert into the customers entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Customer"):
            # grab user form inputs
            fname = request.form["FirstName"]
            lname = request.form["LastName"]
            address1 = request.form["AddressLine1"]
            address2 = request.form["AddressLine2"]
            city = request.form["City"]
            state = request.form["State"]
            zip_code = request.form["ZIP_Code"]
            phone_number = request.form["PhoneNumber"]
        
            # assuming no null inputs
            query = "INSERT INTO Customers (`FirstName`, `LastName`, `AddressLine1`, `AddressLine2`, `City`, `State`, `ZIP_Code`, `PhoneNumber`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(fname, lname, address1, address2, city, state, zip_code, phone_number))
            results = cursor.fetchall()

            return redirect("/customers")

    # Grab Customers data so we send it to our template to display
    if request.method == "GET":
        query = "SELECT * FROM Customers;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        return render_template("customers.html", data=data)


@app.route("/delete-customer/<string:id>")
def delete_customer(id):
    query = "DELETE FROM Customers WHERE CustomerID = '%s';" % (id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    data = cursor.fetchall()

    return redirect("/customers")


@app.route("/edit-customer/<string:id>", methods=["POST", "GET"])
def edit_customer(id):
    if request.method == "GET":
        query = "SELECT * FROM Customers WHERE CustomerID = '%s';" % (id)
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        return render_template("edit_customer.html", data=data)

    if request.method == "POST":
        if request.form.get("Edit_Customer"):
            # grab user form inputs
            fname = request.form["FirstName"]
            lname = request.form["LastName"]
            address1 = request.form["AddressLine1"]
            address2 = request.form["AddressLine2"]
            city = request.form["City"]
            state = request.form["State"]
            zip_code = request.form["ZIP_Code"]
            phone_number = request.form["PhoneNumber"]
            
            query = "UPDATE Customers SET Customers.FirstName = %s, Customers.LastName = %s, Customers.AddressLine1 = %s, Customers.AddressLine2 = %s, Customers.City = %s, Customers.State = %s, Customers.ZIP_Code = %s, Customers.PhoneNumber = %s WHERE Customers.CustomerID = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(fname, lname, address1, address2, city, state, zip_code, phone_number, id))
            data = cursor.fetchall()
            print(data)
            
            return redirect("/customers")


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

        return render_template("flights_has_customers.html", data=data, customer_data=customer_data)
    
    return render_template('flights_has_customers.html')

# TODO:
@app.route('/flights-customers/<int:id>', methods=["POST", "GET"])
def indFlightsCustomers(id):
    if request.method == "GET":

        # Need it to be by flight id
        query = "SELECT * FROM Flights_has_Customers WHERE Flights_FlightID = '%s';" % (id)
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        return render_template("ind_flights_has_customers.html", data=data)


    return render_template('ind_flights_has_customers.html')

# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    port = int(os.environ.get('PORT', 8251))
    app.run(port=port, debug=True)