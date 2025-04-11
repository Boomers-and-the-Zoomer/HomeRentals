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
    Lives CHAR(40),
    Languages CHAR(50),
    Age CHAR(6),
    FunFact CHAR(50),
    ProfilePicture VARCHAR(50),
    CONSTRAINT UserUserAccountFK FOREIGN KEY (Email) REFERENCES UserAccount(Email)
);

CREATE TABLE Session
(
    Token BINARY(16) PRIMARY KEY,
    Email CHAR(30) NOT NULl,
    ExpiryTime DATETIME NOT NULL,
    CONSTRAINT SessionUserFK FOREIGN KEY (Email) REFERENCES UserAccount(Email)
);

CREATE TABLE ResetLink
(
    Token CHAR(30) PRIMARY KEY,
    Email CHAR(30) NOT NULl,
    ExpiryTime DATETIME NOT NULL,
    CONSTRAINT ResetLinkUserFK FOREIGN KEY (Email) REFERENCES UserAccount(Email)
);

CREATE TABLE PropertyListing
(
    PropertyListingID INT PRIMARY KEY AUTO_INCREMENT,
    Email CHAR(30) NOT NULL,
    Address CHAR(100) NOT NULL,
    PostalCode CHAR(10) NOT NULL,
    Description VARCHAR(5000) NOT NULL,
    Price INT NOT NULL,
    Bedrooms INT NOT NULL,
    Beds INT NOT NULL,
    Bathrooms INT NOT NULL,
    SquareMeters INT NOT NULL,
    ParkingSpots INT NOT NULL,
    Kitchens INT NOT NULL,
    RegistrationDate DATE NOT NULL,
    CONSTRAINT PropertyListingUserFK FOREIGN KEY (Email) REFERENCES UserAccount(Email)
);

CREATE TABLE Booking
(
    PropertyListingID INT NOT NULL,
    Email CHAR(30) NOT NULL,
    StartTime DATE NOT NULL,
    EndTime DATE NOT NULL,
    -- TODO: Maybe Email isn't necessary in the primary key
    CONSTRAINT BookingPK PRIMARY KEY (PropertyListingID, Email, StartTime),
    CONSTRAINT BookingPropertyListingFK FOREIGN KEY (PropertyListingID) REFERENCES PropertyListing(PropertyListingID),
    CONSTRAINT BookingUserFK FOREIGN KEY (Email) REFERENCES UserAccount(Email)
);

-- NOTE: This job of this table could be done by a single column in the `Booking` table
--       called `TempExpiryTime` with the type `TIMESTAMP NOT NULL`. A `NULL`-value
--       represents a "finalized" booking, while a non-`NULL` value represents a "temporary"
--       booking that expires at the given timestamp.
CREATE TABLE BookingSession
(
    Token BINARY(16) NOT NULL,
    PropertyListingID INT NOT NULL,
    StartTime DATE NOT NULL,
    EndTime DATE NOT NULL,
    ExpiryTime TIMESTAMP NOT NULL,
    CONSTRAINT BookingSessionPK PRIMARY KEY (Token, PropertyListingID),
    CONSTRAINT BookingSessionSessionFK FOREIGN KEY (Token) REFERENCES Session(Token) ON DELETE CASCADE,
    CONSTRAINT BookingSessionPropertyListingFK FOREIGN KEY (PropertyListingID) REFERENCES PropertyListing(PropertyListingID)
);

CREATE TABLE Picture
(
    PictureID INT AUTO_INCREMENT PRIMARY KEY,
    Filename VARCHAR(50) NOT NULL
);

CREATE TABLE PropertyPicture (
    PropertyListingID INT NOT NULL,
    PictureID INT NOT NULL,
    FOREIGN KEY (PropertyListingID) REFERENCES PropertyListing(PropertyListingID),
    FOREIGN KEY (PictureID) REFERENCES Picture(PictureID),
    PRIMARY KEY (PropertyListingID, PictureID)
);

CREATE TABLE Tag (
    TagID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL
);

CREATE TABLE PropertyTag (
    PropertyListingID INT NOT NULL,
    TagID INT NOT NULL,
    FOREIGN KEY (PropertyListingID) REFERENCES PropertyListing(PropertyListingID),
    FOREIGN KEY (TagID) REFERENCES Tag(TagID),
    PRIMARY KEY (PropertyListingID, TagID)
);

CREATE TABLE Payment (
	PaymentMethod CHAR(20) NOT NULL,
    PaymentTime TIMESTAMP NOT NULL,
    PropertyListingID INT NOT NULL,
    Email CHAR(30) NOT NULL,
    StartTime DATE NOT NULL,
    TotalSum DECIMAL(10,2) NOT NULL,
    PaymentData JSON NOT NULL,
    
    
    CONSTRAINT PaymentPK PRIMARY KEY (PropertyListingID,Email,StartTime),
    CONSTRAINT PaymentBookingFK FOREIGN KEY (PropertyListingID,Email,StartTime) REFERENCES Booking(PropertyListingID,Email,StartTime)
);
