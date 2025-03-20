INSERT INTO UserAccount (Email, PasswordHash) VALUES
-- password: alice123
('alice@example.com', '$argon2id$v=19$m=65536,t=3,p=4$iF3lCPZBIFJHT4tVn5Yz3g$rJb1rl/suzDVeG0lpHw+tojmRiJHzLDdtBE/GM2L7Us'),
-- password: bob123
('bob@example.com', '$argon2id$v=19$m=65536,t=3,p=4$r6iszVqXFfA2Idd9zeCe/g$qt3uC1t5oaSiiJkKE2+t7yVqo40y0T4H5grg+gdlZjo'),
-- password: carol123
('carol@example.com', '$argon2id$v=19$m=65536,t=3,p=4$KMNIFqWNwlwAhm8/MfVDXQ$/4gNW/toVI0DdQ9Kb3tY7hX6mfSl1vfnjDoPzRUdx84'),
-- password: test123
('test.testerson@example.com', '$argon2id$v=19$m=65536,t=3,p=4$PzqPZKSkWFI3WfPZZxwDvg$h3kXj5bZx3VkZZm99SjV6h7DfNZ7GFk98J9SZ9h9WdP'),
-- password: charlie123
('charlie@example.com', '$argon2id$v=19$m=65536,t=3,p=4$AFeFLgCBcb7hSZKr6CcvvQ$utzt36ugME8UeX0ODwlRWreyadLUJnmkWMaOVpNIfG4'),
-- password: diana456
('diana@example.com', '$argon2id$v=19$m=65536,t=3,p=4$fcdLjjxg7Vyy9BIRj0tpwA$NkvT56TsXqAbXcjj2tb/Xie7CIoF07qTA5IgvBB31Gg'),
-- password: emmapass123
('emma@example.com', '$argon2id$v=19$m=65536,t=3,p=4$Psq8sLrssz9Jqupgz6qibQ$ehaPd7jTwGHH/87Jmb+vhVOM5pfjCz50nDTBK2Oduw4'),
-- password: frankthetank
('frank@example.com', '$argon2id$v=19$m=65536,t=3,p=4$4vTDCXOOjaPP7HDF0cdR+g$ms2LpF0pXTrLNpzoR5xEsMf1xZ7O7ZIJS/TozlJi9jg'),
-- password: grace777
('grace@example.com', '$argon2id$v=19$m=65536,t=3,p=4$b4V45zguYg2KQwRrg1ypiA$ej6NW2K8bmHYdZY42WGgskkCDhXk5PFxgnx7gUEmS0I'),
-- password: henryford999
('henry@example.com', '$argon2id$v=19$m=65536,t=3,p=4$PQBDWupWMYX3y9bDrid1dg$BHGZwsMq+sSI+liN3A3U8LmWGKONnVfSU9Vj3/rY7X4');

INSERT INTO User (Email, ExternalID, FirstName, LastName, PhoneNumber, HomeAddress, PostalCode) VALUES
('alice@example.com', 1, 'Alice', 'Smith', '1234567890', '123 Main St, City', '10001'),
('bob@example.com', 2, 'Bob', 'Johnson', '0987654321', '456 Elm St, City', '10002'),
('carol@example.com', 3, 'Carol', 'Williams', '1112223333', '789 Oak St, City', '10003'),
('test.testerson@example.com', 4, 'Test', 'Testerson', '1231231234', '456 Maple St, City', '10004'),
('charlie@example.com', 5, 'Charlie', 'Brown', '222334455', '789 Oak St, City', '10003'),
('diana@example.com', 6, 'Diana', 'Prince', '333445566', '101 Pine St, City', '10004'),
('emma@example.com', 7, 'Emma', 'Watson', '444556677', '202 Maple St, City', '10005'),
('frank@example.com', 8, 'Frank', 'Castle', '555667788', '303 Birch St, City', '10006'),
('grace@example.com', 9, 'Grace', 'Kelly', '666778899', '404 Cedar St, City', '10007'),
('henry@example.com', 10, 'Henry', 'Ford', '777889900', '505 Walnut St, City', '10008');

INSERT INTO Session (Token, Email, ExpiryTime) VALUES
(UNHEX('4D79536563726574546F6B656E4F6E65'), 'alice@example.com', '2025-12-31 23:59:59'),
(UNHEX('4D79536563726574546F6B656E54776F'), 'bob@example.com', '2025-12-31 23:59:59');

INSERT INTO ResetLink (Token, Email, ExpiryTime) VALUES
('abcd1234', 'alice@example.com', '2025-12-31 23:59:59'),
('efgh5678', 'bob@example.com', '2025-12-31 23:59:59');

INSERT INTO PropertyListing (Email, Address, PostalCode, Description, Bedrooms, Beds, Bathrooms, SquareMeters, ParkingSpots, Kitchens) VALUES
('alice@example.com', '123 Main St, City', '10001', 'A nice little place to stay the night.', 3, 4, 2, 120, 1, 1),
('bob@example.com', '456 Elm St, City', '10002', 'It may look a little shabby, but it''s a perfectly quaint apartment.', 2, 2, 1, 80, 0, 1),
('charlie@example.com', '789 Oak St, City', '10003', 'A spacious house with a beautiful garden.', 4, 5, 3, 200, 2, 1),
('diana@example.com', '101 Pine St, City', '10004', 'Modern apartment in the heart of downtown.', 2, 3, 1, 90, 0, 1),
('emma@example.com', '202 Maple St, City', '10005', 'A cozy cabin perfect for a weekend getaway.', 3, 4, 2, 110, 1, 1),
('frank@example.com', '303 Birch St, City', '10006', 'A luxury villa with ocean views.', 5, 6, 4, 300, 3, 2),
('grace@example.com', '404 Cedar St, City', '10007', 'A charming cottage in a quiet neighborhood.', 3, 3, 2, 100, 1, 1),
('henry@example.com', '505 Walnut St, City', '10008', 'A sleek modern loft with open-concept living.', 1, 1, 1, 70, 0, 1);

INSERT INTO Booking (PropertyListingID, Email, StartTime, EndTime) VALUES
(1, 'carol@example.com', '2025-05-01 12:00:00', '2025-05-07 12:00:00'),
(2, 'alice@example.com', '2025-06-01 12:00:00', '2025-06-07 12:00:00'),
(1, 'test.testerson@example.com', '2025-07-01 12:00:00', '2025-07-07 12:00:00');


