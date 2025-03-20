DROP SCHEMA IF EXISTS HomeRentals;
CREATE SCHEMA HomeRentals;

USE HomeRentals;

CREATE TABLE UserAccount
(
    Email CHAR(30) PRIMARY KEY,
    PasswordHash CHAR(128) NOT NULL
);

CREATE TABLE User
(
    Email CHAR(30) PRIMARY KEY,
    ExternalID INT UNIQUE AUTO_INCREMENT NOT NULL,
    FirstName CHAR(30) NOT NULL,
    LastName CHAR(30) NOT NULL,
    PhoneNumber CHAR(16) NOT NULL,
    HomeAddress CHAR(100) NOT NULL,
    PostalCode CHAR(10) NOT NULL,
    CONSTRAINT UserUserAccountFK FOREIGN KEY (Email) REFERENCES UserAccount(Email)
);

CREATE TABLE Session
(
    Token BINARY(16) PRIMARY KEY,
    Email CHAR(30) NOT NULl,
    ExpiryTime DATETIME NOT NULL,
    CONSTRAINT SessionUserFK FOREIGN KEY (Email) REFERENCES User(Email)
);

CREATE TABLE ResetLink
(
    Token CHAR(30) PRIMARY KEY,
    Email CHAR(30) NOT NULl,
    ExpiryTime DATETIME NOT NULL,
    CONSTRAINT ResetLinkUserFK FOREIGN KEY (Email) REFERENCES User(Email)
);

CREATE TABLE PropertyListing
(
    PropertyListingID INT PRIMARY KEY AUTO_INCREMENT,
    Email CHAR(30) NOT NULL,
    Address CHAR(100) NOT NULL,
    PostalCode CHAR(10) NOT NULL,
    Description VARCHAR(5000) NOT NULL,
    Bedrooms INT NOT NULL,
    Beds INT NOT NULL,
    Bathrooms INT NOT NULL,
    SquareMeters INT NOT NULL,
    ParkingSpots INT NOT NULL,
    Kitchens INT NOT NULL,
    CONSTRAINT PropertyListingUserFK FOREIGN KEY (Email) REFERENCES User(Email)
);

CREATE TABLE Booking
(
    PropertyListingID INT NOT NULL,
    Email CHAR(30) NOT NULL,
    StartTime TIMESTAMP NOT NULL,
    EndTime TIMESTAMP NOT NULL,
    CONSTRAINT BookingPK PRIMARY KEY (PropertyListingID, Email, StartTime),
    CONSTRAINT BookingPropertyListingFK FOREIGN KEY (PropertyListingID) REFERENCES PropertyListing(PropertyListingID),
    CONSTRAINT BookingUserFK FOREIGN KEY (Email) REFERENCES User(Email)
);

-- NOTE: This job of this table could be done by a single column in the `Booking` table
--       called `TempExpiryTime` with the type `TIMESTAMP NOT NULL`. A `NULL`-value
--       represents a "finalized" booking, while a non-`NULL` value represents a "temporary"
--       booking that expires at the given timestamp.
CREATE TABLE BookingSession
(
    Token BINARY(16) NOT NULL,
    PropertyListingID INT NOT NULL,
    StartTime TIMESTAMP NOT NULL,
    EndTime TIMESTAMP NOT NULL,
    ExpiryTime TIMESTAMP NOT NULL,
    CONSTRAINT BookingSessionPK PRIMARY KEY (Token, PropertyListingID, StartTime),
    CONSTRAINT BookingSessionSessionFK FOREIGN KEY (Token) REFERENCES Session(Token),
    CONSTRAINT BookingSessionPropertyListingFK FOREIGN KEY (PropertyListingID) REFERENCES PropertyListing(PropertyListingID)
);

CREATE TABLE Picture
(
    PictureID INT AUTO_INCREMENT PRIMARY KEY,
    Filename VARCHAR(50) NOT NULL
);



