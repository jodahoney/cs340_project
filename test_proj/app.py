from flask import Flask, render_template, json, request, redirect
import database.db_connector as db
import os

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
# app.config['MYSQL_USER'] = 'cs340_dehoneyj'
# app.config['MYSQL_PASSWORD'] = '2584' #last 4 of onid
# app.config['MYSQL_DB'] = 'cs340_dehoneyj'
# app.config['MYSQL_CURSORCLASS'] = "DictCursor"

# Routes 

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/orcas')
def orcas():

    query = "SELECT * FROM Flights;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("flights.html", flights=results)

# route for people page
@app.route("/airports", methods=["POST", "GET"])
def airports():

    # insert a person into the airports entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Airport"):
            # grab user form inputs
            airportID = request.form["airportID"]
            name = request.form["name"]
            city = request.form["city"]
            state = request.form["state"]
        
            # assuming no null inputs
            query = "INSERT INTO Airports (airportID, name, city, state) VALUES (%s, %s,%s,%s);"
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
@app.route("/delete_airport/<int:id>")
def delete_airport(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Airports WHERE id = '%s';"
    cur = db.connection.cursor()
    cur.execute(query, (id,))
    db.connection.commit()

    # redirect back to airport page
    return redirect("/airports")


# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_airport/<int:id>", methods=["POST", "GET"])
def edit_airport(id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Airports WHERE id = %s" % (id)
        cur = db.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_airport.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit airport' button
        if request.form.get("Edit_Airport"):
            # grab user form inputs
            airportID = request.form["airportID"]
            name = request.form["name"]
            city = request.form["city"]
            state = request.form["state"]

            query = "UPDATE Airports SET Airports.name = %s, Airports.city = %s, Airports.state = %s WHERE Airports.airportID = %s"
            cur = db.connection.cursor()
            cur.execute(query, (name, city, state, airportID))
            db.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/people")

            

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)