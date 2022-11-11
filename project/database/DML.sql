-- Airplane Querys
    -- Get all airplanes
    SELECT * FROM Airplanes;
    -- Search for an airplane by tail number
    SELECT * FROM Airplanes WHERE Airplanes.TailNumber = `:TailNumberInputFromSearch`;
    -- Add new airplane
    INSERT INTO Airplanes (`TailNumber`, `Make`, `Model`, `Range`, `FuelCapacity`, `LastMaintenancePerformed`, `MaintenanceFrequency`)
        VALUES (`:TailNumberInput`, `:MfgDropdownInput`, `:MakeInput`, `:RangeInMilesInput`, `:FuelCapacityInGalInput`, `:LastMaintenancePerformedInput`, `:MaintenanceFrequencyInput`);
    -- Update LastMaintenancePerformed
    UPDATE Airplanes SET `LastMaintenancePerformed` = `:LastMaintenancePerformedInput`;
    -- Delete an Airplane
    DELETE FROM Airplanes WHERE Airplanes.TailNumber = `:TailNumberInputFromUser`;

-- Airport Querys
    -- Get all airport
    SELECT * FROM Airports;
    -- Search for an Airport by city
    SELECT * FROM Airports WHERE Airports.City = `:AirportCityInputFromUser`;
    -- Add a new airport
    INSERT INTO Airports (`AirportID`, `Name`, `City`, `State`) 
        VALUES (`:AirportIDInput`, `:NameInput`, `:CityInput`, `:StateDropdownInput`);
    -- Update Airport info
    UPDATE Airports SET `AirportID` = ':AirportIDInput', `Name` = `:NameInput`, `City` = `:CityInput`, `State` = `:StateDropdownInput`;
    -- Delete Airport 
    DELETE FROM Airports WHERE Airports.AirportID = `:AirportIDToDeleteFromUser`;

-- Pilots Querys
    -- Get all pilots
    SELECT * FROM Pilots;
    -- Search for Pilot by first name
    SELECT * FROM Pilots WHERE Pilots.FirstName = `:FirstNameSearch`;
    -- Add new pilot
    INSERT INTO Pilots (`FirstName`, `LastName`, `PhoneNumber`)
        VALUES (:`FirstNameInput`, :`LastNameInput`, :`PhoneNumberInput`);
    -- Delete a pilot by ID
    DELETE FROM Pilots WHERE Pilots.PilotID = `:PilotIDToDeleteFromUser`;

-- Customer Querys
    -- Get all customers
    SELECT * FROM Customers;
    -- Add new customer
    INSERT INTO Customers (`FirstName`, `LastName`, `AddressLine1`, `AddressLine2`, `City`, `State`, `ZIP_Code`, `PhoneNumber`)
        VALUES (`:FirstNameInput`, `:LastNameInput`, `:AddressLine1Input`, `:AddressLine2Input`, `:CityInput`, `:StateDropdownInput`, `:ZIP_Code`, `:PhoneNumberInput`);
    -- Delete Customer by ID
    DELETE FROM Customers WHERE Customers.CustomerID = `:CustomerIDToDeleteFromUser`;
    -- Associate Flight with Customer
    INSERT INTO Flights_has_Customers (`Flights_FlightID`, `Customers_CustomerID`)
        VALUES (`:FlightIDInputFromDropdown`, `CustomerIDInputFromDropdown`);
    -- Disassociate Customer with Flight
    DELETE FROM Flights_has_Customers WHERE 
        Flights_has_Customers.Flights_FlightID = `:FlightIDInputFromUser` 
        AND 
        Flights_has_Customers.Customers_CustomerID = `:CustomerIDInputFromUser`;

-- Flight Querys
    -- Get all flights
    SELECT * FROM Flights;
    -- Search for flight by flightNumber
    SELECT * FROM Flights WHERE Flights.FlightID = `:FlightNumberSearch`;
    -- Add new flight
    INSERT INTO Flights (`FlightID`, `Origin`, `Destination`, `Departure`, `Arrival`, `FlightDuration`, `Pilot`, `CoPilot`, `Aircraft`)
        VALUES (`:FlightIDInputFromUser`, `:OriginAirportDropdown`, `:DestinationAirportDropdown`, `:DepartureTimeInput`, `:ArrivalTimeInput`, `:FlightDurationInput`, `:PilotDropdown`, `:CopilotDropdown`, `:AircraftDropdown`);
    -- Update flight departure and arrival time
    UPDATE Flights SET Departure = `:NewDepartureTimeInput` AND Arrival = `:NewArrivalTimeInput`;
    -- Get all customers on a selected flight number
    SELECT Customers.FirstName, Customers.LastName FROM Flights, Flights_has_Customers, Customers
    WHERE Flights.FlightID = `:FlightNumberDropDown`
    GROUP BY Customers.FirstName;
    -- Delete a flight by ID
    DELETE FROM Flights WHERE Flights.FlightID = `:FlightNumberToDeleteFromUser`;

