from flask import Flask, render_template, json, request, redirect
import database.db_connector as db
import os

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

app.config['MYSQL_CURSORCLASS'] = "DictCursor"

# Routes 

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/orcas')
def orcas():
    # Show all flights
    query = "SELECT * FROM Flights;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("flights.html", flights=results)

# Implementation for Airports
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


# route for delete functionality, deleting an airport
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete-airport/<string:id>")
def delete_airport(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Airports WHERE AirportID = '%s';" % (id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    data = cursor.fetchall()

    # redirect back to airport page
    return redirect("/airports")


# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
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
            
# Implementation for Airplanes
@app.route("/airplanes", methods=["POST", "GET"])
def airplanes():

    # insert into the airports entity
    if request.method == "POST":
        # fire off if user presses the Add airplane button
        if request.form.get("Add_Airplanes"):
            # grab user form inputs
            tail_number = request.form["TailNumber"]
            make = request.form["Make"]
            model = request.form["Model"]
            range = request.form["Range"]
            fuel_capacity = request.form["FuelCapacity"]
            last_maintenance_performed = request.form["LastMaintenancePerformed"]
            maintenance_frequency = request.form["MaintenanceFrequency"]
        
            # assuming no null inputs
            query = "INSERT INTO Airplanes (TailNumber, Make, Model, Range, FuelCapacity, LastMaintenancePerformed, MaintenanceFrequency) VALUES (%s, %s, %s, %i, %i, %d. %i);"
            # cur = db.connection.cursor()
            # cur.execute(query, (airportID, name, city, state))
            # db.connection.commit()
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(tail_number, make, model, range, fuel_capacity, last_maintenance_performed, maintenance_frequency))
            results = cursor.fetchall()

            return redirect("/airplanes")

    # Grab Airports data so we send it to our template to display
    if request.method == "GET":
        # db query to grab all the people in bsg_people
        query = "SELECT * FROM Airplanes;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("airplanes.html", data=data)


# route for delete functionality, deleting an airplane
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete-airplane/<string:id>")
def delete_airplane(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Airplanes WHERE TailNumber = '%s';" % (id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    data = cursor.fetchall()

    # redirect back to airport page
    return redirect("/airplanes")


# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit-airplane/<string:id>", methods=["POST", "GET"])
def edit_airplane(id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Airplanes WHERE TailNumber = '%s';" % (id)
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        return render_template("edit_airplane.html", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        if request.form.get("Edit_Airplane"):
            # grab user form inputs
            tail_number = request.form["TailNumber"]
            make = request.form["Make"]
            model = request.form["Model"]
            range = request.form["Range"]
            fuel_capacity = request.form["FuelCapacity"]
            last_maintenance_performed = request.form["LastMaintenancePerformed"]
            maintenance_frequency = request.form["MaintenanceFrequency"]
            
            # . UPDATE table_name SET column1 = value1, column2 = value2 WHERE id=100;
            query = "UPDATE Airplanes SET Airplanes.TailNumber = %s, Airplanes.Make = %s, Airplanes.Model = %s, Airplanes.Range = %i, Airplanes.FuelCapacity = %i, Airplanes.LastMaintenancePerformed = %d, Airplanes.MaintenanceFrequency = %i WHERE Airplanes.TailNumber = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(tail_number, make, model, range, fuel_capacity, last_maintenance_performed, maintenance_frequency))
            data = cursor.fetchall()
            print(data)
            # redirect back to people page after we execute the update query
            return redirect("/airplanes")
            



# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)