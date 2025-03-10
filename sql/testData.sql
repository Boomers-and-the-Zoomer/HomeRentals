
INSERT INTO User (Email, ExternalID, FirstName, LastName, PhoneNumber, HomeAdress, PostalCode) VALUES
('alice@example.com', 1, 'Alice', 'Smith', '1234567890', '123 Main St, City', '10001'),
('bob@example.com', 2, 'Bob', 'Johnson', '0987654321', '456 Elm St, City', '10002'),
('carol@example.com', 3, 'Carol', 'Williams', '1112223333', '789 Oak St, City', '10003');


INSERT INTO Session (Token, Email, ExpiryTime) VALUES
(UNHEX('4D79536563726574546F6B656E4F6E65'), 'alice@example.com', '2025-12-31 23:59:59'),
(UNHEX('4D79536563726574546F6B656E54776F'), 'bob@example.com', '2025-12-31 23:59:59');


INSERT INTO ResetLink (Link, Email, ExpiryTime) VALUES
('https://example.com/reset?token=abcd1234', 'alice@example.com', '2025-12-31 23:59:59'),
('https://example.com/reset?token=efgh5678', 'bob@example.com', '2025-12-31 23:59:59');


INSERT INTO PropertyListing (Email, Address, PostalCode, Bedrooms, Bathrooms, SquareMeters, ParkingSpots, Kitchens) VALUES
('alice@example.com', '123 Main St, City', '10001', 3, 2, 120, 1, 1),
('bob@example.com', '456 Elm St, City', '10002', 2, 1, 80, 0, 1);


INSERT INTO Booking (PropertyListingID, Email, StartTime, EndTime) VALUES
(1, 'carol@example.com', '2025-05-01 12:00:00', '2025-05-07 12:00:00'),
(2, 'alice@example.com', '2025-06-01 12:00:00', '2025-06-07 12:00:00');

