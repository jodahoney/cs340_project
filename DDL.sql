-- MySQL Workbench Forward Engineering

SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

-- -----------------------------------------------------
-- Table `Airplanes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Airplanes` ;

CREATE TABLE IF NOT EXISTS `Airplanes` (
  `TailNumber` VARCHAR(6) NOT NULL,
  `Make` VARCHAR(45) NOT NULL,
  `Model` VARCHAR(45) NOT NULL,
  `Range` INT NOT NULL,
  `FuelCapacity` INT NOT NULL,
  `LastMaintenancePerformed` DATE NOT NULL,
  `MaintenanceFrequency` INT NOT NULL,
  `NextMaintenanceDate` DATE  NOT NULL,
  PRIMARY KEY (`TailNumber`),
  UNIQUE INDEX `TailNumber_UNIQUE` (`TailNumber` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Pilots`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Pilots` ;

CREATE TABLE IF NOT EXISTS `Pilots` (
  `PilotID` INT NOT NULL AUTO_INCREMENT,
  `FirstName` VARCHAR(45) NOT NULL,
  `LastName` VARCHAR(45) NOT NULL,
  `PhoneNumber` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`PilotID`),
  UNIQUE INDEX `PilotID_UNIQUE` (`PilotID` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Airports`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Airports` ;

CREATE TABLE IF NOT EXISTS `Airports` (
  `AirportID` VARCHAR(3) NOT NULL,
  `Name` VARCHAR(45) NOT NULL,
  `City` VARCHAR(45) NOT NULL,
  `State` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`AirportID`),
  UNIQUE INDEX `AirportID_UNIQUE` (`AirportID` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Flights`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Flights` ;

CREATE TABLE IF NOT EXISTS `Flights` (
  `FlightID` INT NOT NULL AUTO_INCREMENT,
  `Origin` VARCHAR(3) NOT NULL,
  `Destination` VARCHAR(3) NOT NULL,
  `Departure` DATETIME NOT NULL,
  `Arrival` DATETIME NOT NULL,
  `FlightDuration` INT NOT NULL,
  `Pilot` INT NOT NULL,
  `CoPilot` INT NOT NULL,
  `Aircraft` VARCHAR(6) NOT NULL,
  PRIMARY KEY (`FlightID`),
  UNIQUE INDEX `FlightID_UNIQUE` (`FlightID` ASC) VISIBLE,
  INDEX `Aircraft_idx` (`Aircraft` ASC) VISIBLE,
  INDEX `Pilot_idx` (`Pilot` ASC) VISIBLE,
  INDEX `Origin_idx` (`Origin` ASC) VISIBLE,
  INDEX `Destination_idx` (`Destination` ASC) VISIBLE,
  INDEX `CoPilot_idx` (`CoPilot` ASC) VISIBLE,
  CONSTRAINT `Aircraft`
    FOREIGN KEY (`Aircraft`)
    REFERENCES `Airplanes` (`TailNumber`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Pilot`
    FOREIGN KEY (`Pilot`)
    REFERENCES `Pilots` (`PilotID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Origin`
    FOREIGN KEY (`Origin`)
    REFERENCES `Airports` (`AirportID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Destination`
    FOREIGN KEY (`Destination`)
    REFERENCES `Airports` (`AirportID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `CoPilot`
    FOREIGN KEY (`CoPilot`)
    REFERENCES `Pilots` (`PilotID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Customers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Customers` ;

CREATE TABLE IF NOT EXISTS `Customers` (
  `CustomerID` INT NOT NULL AUTO_INCREMENT,
  `FirstName` VARCHAR(45) NOT NULL,
  `LastName` VARCHAR(45) NOT NULL,
  `AddressLine1` VARCHAR(45) NOT NULL,
  `AddressLine2` VARCHAR(45),
  `City` VARCHAR(45) NOT NULL,
  `State` VARCHAR(45) NOT NULL,
  `ZIP_Code` INT(5) NOT NULL,
  `PhoneNumber` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`CustomerID`),
  UNIQUE INDEX `CustomerID_UNIQUE` (`CustomerID` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Flights_has_Customers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Flights_has_Customers` ;

CREATE TABLE IF NOT EXISTS `Flights_has_Customers` (
  `flights_has_customersID` INT NOT NULL AUTO_INCREMENT,
  `Flights_FlightID` INT NOT NULL,
  `Customers_CustomerID` INT,
  PRIMARY KEY (`flights_has_customersID`),
  INDEX `fk_Flights_has_Customers_Customers1_idx` (`Customers_CustomerID` ASC) VISIBLE,
  INDEX `fk_Flights_has_Customers_Flights1_idx` (`Flights_FlightID` ASC) VISIBLE,
  UNIQUE INDEX `flights_has_customersID_UNIQUE` (`flights_has_customersID` ASC) VISIBLE,
  CONSTRAINT `fk_Flights_has_Customers_Flights1`
    FOREIGN KEY (`Flights_FlightID`)
    REFERENCES `Flights` (`FlightID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Flights_has_Customers_Customers1`
    FOREIGN KEY (`Customers_CustomerID`)
    REFERENCES `Customers` (`CustomerID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Data for table `Airplanes`
-- -----------------------------------------------------
INSERT INTO `Airplanes` (`TailNumber`, `Make`, `Model`, `Range`, `FuelCapacity`, `LastMaintenancePerformed`, `MaintenanceFrequency`, `NextMaintenanceDate`) 
	VALUES ('N83RF', 'Boeing', '717', 2371, 3673, '2022-01-23', 365, 
  (SELECT DATE_ADD('2022-01-23', INTERVAL 365 DAY))),
	('N163NU', 'Bombardier', 'Q400', 1268, 835, '2022-10-01', 180,
  (SELECT DATE_ADD('2022-10-01', INTERVAL 180 DAY))),
	('N76901', 'Airbus', 'A320', 5740, 7185, '2022-09-01', 90,
  (SELECT DATE_ADD('2022-09-01', INTERVAL 90 DAY))),
	('N314T', 'Boeing', '737', 3000, 6878, '2022-09-30', 90,
  (SELECT DATE_ADD('2022-09-30', INTERVAL 90 DAY)));

-- -----------------------------------------------------
-- Data for table `Airports`
-- -----------------------------------------------------
INSERT INTO `Airports` (`AirportID`, `Name`, `City`, `State`) 
	VALUES ('SEA', 'Seattle-Tacoma International Airport', 'Seattle', 'Washington'),
	('PDX', 'Portland International Airport', 'Portland', 'Oregon'),
	('SFO', 'San Francisco International Airport', 'San Francisco', 'California'),
	('BOI', 'Boise Airport', 'Boise', 'Idaho'),
	('FCA', 'Glacier Park International Airport', 'Kalispell', 'Montana');

-- -----------------------------------------------------
-- Data for table `Pilots`
-- -----------------------------------------------------
INSERT INTO `Pilots` (`FirstName`, `LastName`, `PhoneNumber`)
  VALUES ('Steve', 'Morton', '222-356-8245'),
  ('John', 'Woodward', '206-548-1255'),
  ('Ryan', 'Kawalski', '908-457-8404');

-- -----------------------------------------------------
-- Data for table `Flights`
-- -----------------------------------------------------
INSERT INTO `Flights` (`FlightID`, `Origin`, `Destination`, `Departure`, `Arrival`, `FlightDuration`, `Pilot`, `CoPilot`, `Aircraft`) 
	VALUES (90, (SELECT AirportID FROM Airports WHERE AirportID = 'SEA'), 
		(SELECT AirportID FROM Airports WHERE AirportID = 'PDX'), 
		'2022/04/22 21:50:25', '2022/04/22 22:50:25', 60, 
		(SELECT PilotID FROM Pilots WHERE PilotID = 1), 
		(SELECT PilotID FROM Pilots WHERE PilotID = 2),
		(SELECT TailNumber FROM Airplanes WHERE TailNumber = 'N83RF')),
	(62, (SELECT AirportID FROM Airports WHERE AirportID = 'SEA'), 
		(SELECT AirportID FROM Airports WHERE AirportID = 'BOI'), 
		'2022/06/22 06:00:16', '2022/06/22 07:00:16', 60, 
		(SELECT PilotID FROM Pilots WHERE PilotID = 3), 
		(SELECT PilotID FROM Pilots WHERE PilotID = 2), 
		(SELECT TailNumber FROM Airplanes WHERE TailNumber = 'N314T')),
	(274, (SELECT AirportID FROM Airports WHERE AirportID = 'SEA'), 
		(SELECT AirportID FROM Airports WHERE AirportID = 'SFO'), 
		'2022/05/16 21:50:57', '2022/05/16 23:50:57', 120, 
		(SELECT PilotID FROM Pilots WHERE PilotID = 1), 
		(SELECT PilotID FROM Pilots WHERE PilotID = 3), 
		(SELECT TailNumber FROM Airplanes WHERE TailNumber = 'N76901'));

-- -----------------------------------------------------
-- Data for table `Customers`
-- -----------------------------------------------------
INSERT INTO `Customers` (`FirstName`, `LastName`, `AddressLine1`, `City`, `State`, `ZIP_Code`, `PhoneNumber`) 
	VALUES ('John', 'Smoth', '1234 Holden Ave SW', 'Seattle', 'WA', 98125, '206-333-5555'),
	('James', 'Polk', '80 Raging River Way', 'Detroit', 'MI', 48126, '313-918-5486'),
	('Laura', 'Croft', '640 Rainier Ave SW', 'Bellevue', 'WA', 98149, '206-443-9856');

-- -----------------------------------------------------
-- Data for table `Flights_has_Customers`
-- -----------------------------------------------------
INSERT INTO `Flights_has_Customers` (`Flights_FlightID`, `Customers_CustomerID`) 
	VALUES ((SELECT FlightID FROM Flights WHERE FlightID = 90),(SELECT CustomerID FROM Customers WHERE CustomerID = 1)),
	((SELECT FlightID FROM Flights WHERE FlightID = 90), (SELECT CustomerID FROM Customers WHERE CustomerID = 2)),
	((SELECT FlightID FROM Flights WHERE FlightID = 90), (SELECT CustomerID FROM Customers WHERE CustomerID = 3));



SET FOREIGN_KEY_CHECKS=1;
COMMIT;