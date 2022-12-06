from flask import Flask, render_template, json, request, redirect
import database.db_connector as db
import datetime
import os

app = Flask(__name__)
db_connection = db.connect_to_database()

app.config['MYSQL_CURSORCLASS'] = "DictCursor"


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
            next_maintenance_date = datetime.datetime.strptime(last_maintenance_performed, "%Y-%m-%d") + datetime.timedelta(days = int(maintenance_frequency))
        
            # assuming no null inputs
            query = "INSERT INTO Airplanes (`TailNumber`, `Make`, `Model`, `Range`, `FuelCapacity`, `LastMaintenancePerformed`, `MaintenanceFrequency`, `NextMaintenanceDate`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(tail_number, make, model, air_range, fuel_capacity, last_maintenance_performed, maintenance_frequency, next_maintenance_date))
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
            next_maintenance_date = datetime.datetime.strptime(last_maintenance_performed, "%Y-%m-%d") + datetime.timedelta(days = int(maintenance_frequency))
           
            query = "UPDATE Airplanes SET Airplanes.Make = %s, Airplanes.Model = %s, Airplanes.Range = %s, Airplanes.FuelCapacity = %s, Airplanes.LastMaintenancePerformed = %s, Airplanes.MaintenanceFrequency = %s, Airplanes.NextMaintenanceDate = %s WHERE Airplanes.TailNumber = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(make, model, range, fuel_capacity, last_maintenance_performed, maintenance_frequency, next_maintenance_date, id))
            data = cursor.fetchall()
            print(data)
 
            return redirect("/airplanes")


@app.route("/flights", methods=["POST", "GET"])
def flights():
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
            Customers = request.form.getlist("customer-check")

            
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

        query6 = "SELECT Customers_CustomerID FROM Flights_has_Customers WHERE Flights_FlightID = %s;" % (id)
        cursor = db.execute_query(db_connection=db_connection, query=query6)
        flight_has_cust_data = cursor.fetchall()
        # change dictionary to list of customer ID's related to flightID
        flight_has_cust_data = [line['Customers_CustomerID'] for line in flight_has_cust_data]

        return render_template("edit_flight.html", 
            data=data, 
            customer_data=customer_data, 
            airport_data=airport_data,
            pilot_data=pilot_data,
            aircraft_data=aircraft_data,
            flight_has_cust_data=flight_has_cust_data)

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
            Customers = request.form.getlist("customer-check")

            FlightDuration = calculate_flight_time(Arrival, Departure)
        
            query = "UPDATE Flights SET Flights.Origin = %s, Flights.Destination = %s, Flights.Departure = %s, \
                Flights.Arrival = %s, Flights.FlightDuration = %s, Flights.Pilot = %s, Flights.CoPilot = %s, Flights.Aircraft = %s \
                WHERE Flights.FlightID = %s;"
            cursor = db.execute_query(db_connection=db_connection,
                query=query,
                query_params=(Origin, Destination, Departure, Arrival, FlightDuration, Pilot, CoPilot, Aircraft, id)
            )
            data = cursor.fetchall()

            # Get current list of customers to compare with newest submission
            query6 = "SELECT Customers_CustomerID FROM Flights_has_Customers WHERE Flights_FlightID = %s;" % (id)
            cursor = db.execute_query(db_connection=db_connection, query=query6)
            flight_has_cust_data = cursor.fetchall()
            prev_cust_data = [line['Customers_CustomerID'] for line in flight_has_cust_data]

            new_cust_data = list(map(int, Customers))

            # if there is a change in the customers list
            if new_cust_data != prev_cust_data:
                # if they removed customers
                if len(new_cust_data) < len(prev_cust_data):
                    # remove the customers 
                    prev_cust_set = set(prev_cust_data)
                    removed_customers = [x for x in prev_cust_set if x not in new_cust_data]

                    # delete the removed customers from the intersection table
                    for cust in removed_customers:
                        del_query = "DELETE FROM Flights_has_Customers \
                            WHERE Flights_FlightID = '%s' AND Customers_CustomerID = '%s';" % (id, cust)
                        cursor = db.execute_query(db_connection=db_connection, query=del_query)

                # if they added customers, then insert to intersection table
                elif len(new_cust_data) > len(prev_cust_data):
                    new_cust_set = set(new_cust_data)
                    added_customers = [x for x in new_cust_set if x not in prev_cust_data]

                    for cust in added_customers:
                        add_query = "INSERT INTO Flights_has_Customers \
                            (Flights_FlightID, Customers_CustomerID) \
                            VALUES (%s, %s);"
                        cursor = db.execute_query(db_connection=db_connection, query=add_query, query_params=(id, cust))
                
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

        query2 = "SELECT * FROM Customers;"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        customer_data = cursor.fetchall()

        return render_template("flights_has_customers.html", data=data, customer_data=customer_data)
    
    return render_template('flights_has_customers.html')

@app.route('/ind-flights-customers/<int:flight_id>', methods=["POST", "GET"])
def indFlightsCustomers(flight_id):
    if request.method == "GET":

        query = "SELECT * FROM Flights_has_Customers WHERE Flights_FlightID = '%s';" % (flight_id)
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        query2 = "SELECT * FROM Customers;"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        customer_data = cursor.fetchall()

        query3 = "SELECT * FROM Flights WHERE FlightID = '%s';" % (flight_id)
        cursor = db.execute_query(db_connection=db_connection, query=query3)
        flight_data = cursor.fetchone()

        return render_template("ind_flights_has_customers.html", 
            data=data, 
            customer_data=customer_data,
            flight_data=flight_data)

# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    port = int(os.environ.get('PORT', 8251))
    app.run(port=port, debug=True)