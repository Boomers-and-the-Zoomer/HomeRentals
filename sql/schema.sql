DROP SCHEMA IF EXISTS HomeRentals;
CREATE SCHEMA HomeRentals;

USE HomeRentals;

CREATE TABLE User
(
    Email CHAR(30) PRIMARY KEY,
    ExternalID INT UNIQUE NOT NULL,
    FirstName CHAR(30) NOT NULL,
    LastName CHAR(30) NOT NULL,
    PhoneNumber CHAR(16) NOT NULL,
    HomeAdress CHAR(100) NOT NULL,
    PostalCode CHAR(10) NOT NULL
);

CREATE TABLE Session
(
    Token BINARY(16) PRIMARY KEY,
    Email CHAR(30) NOT NULl,
    ExpiryTime TIMESTAMP NOT NULL,
    CONSTRAINT SessionUserFK FOREIGN KEY (Email) REFERENCES User(Email)
);

CREATE TABLE ResetLink
(
    Link CHAR(100) PRIMARY KEY,
    Email CHAR(30) NOT NULl,
    ExpiryTime TIMESTAMP NOT NULL,
    CONSTRAINT ResetLinkUserFK FOREIGN KEY (Email) REFERENCES User(Email)
);

CREATE TABLE PropertyListing
(
    PropertyListingID INT PRIMARY KEY AUTO_INCREMENT,
    Email CHAR(30) NOT NULL,
    Address CHAR(100) NOT NULL,
    PostalCode CHAR(10) NOT NULL,
    Bedrooms INT NOT NULL,
    Bathrooms INT NOT NULL,
    SquareMeters INT NOT NULL,
    ParkingSpots INT,
    Kitchens INT,
    CONSTRAINT PropertyListingUserFK FOREIGN KEY (Email) REFERENCES User(Email)
);

CREATE TABLE Booking
(
    PropertyListingID INT NOT NULL,
    Email CHAR(30),
    StartTime TIMESTAMP,
    EndTime TIMESTAMP,
    CONSTRAINT BookingPK PRIMARY KEY (PropertyListingID, Email, StartTime),
    CONSTRAINT BookingPropertyListingFK FOREIGN KEY (PropertyListingID) REFERENCES PropertyListing(PropertyListingID),
    CONSTRAINT BookingUserFK FOREIGN KEY (Email) REFERENCES User(Email)
);

