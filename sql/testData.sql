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

INSERT INTO User (Email, ExternalID, FirstName, LastName, PhoneNumber, HomeAddress, PostalCode, Lives, Languages, Age, FunFact) VALUES
('alice@example.com', 1, 'Alice', 'Smith', '1234567890', '123 Main St, City', '10001','Oslo, Norway', 'Norwegian, English, Spanish', '40s', 'Loves Smash'),
('bob@example.com', 2, 'Bob', 'Johnson', '0987654321', '456 Elm St, City', '10002',NULL, NULL, NULL, NULL),
('carol@example.com', 3, 'Carol', 'Williams', '1112223333', '789 Oak St, City', '10003', NULL, NULL, NULL, NULL),
('test.testerson@example.com', 4, 'Test', 'Testerson', '1231231234', '456 Maple St, City', '10004', NULL, NULL, NULL, NULL),
('charlie@example.com', 5, 'Charlie', 'Brown', '222334455', '789 Oak St, City', '10003', NULL, NULL, NULL, NULL),
('diana@example.com', 6, 'Diana', 'Prince', '333445566', '101 Pine St, City', '10004', NULL, NULL, NULL, NULL),
('emma@example.com', 7, 'Emma', 'Watson', '444556677', '202 Maple St, City', '10005', NULL, NULL, NULL, NULL),
('frank@example.com', 8, 'Frank', 'Castle', '555667788', '303 Birch St, City', '10006', NULL, NULL, NULL, NULL),
('grace@example.com', 9, 'Grace', 'Kelly', '666778899', '404 Cedar St, City', '10007', NULL, NULL, NULL, NULL),
('henry@example.com', 10, 'Henry', 'Ford', '777889900', '505 Walnut St, City', '10008', NULL, NULL, NULL, NULL);

INSERT INTO Session (Token, Email, ExpiryTime) VALUES
(UNHEX('4D79536563726574546F6B656E4F6E65'), 'alice@example.com', '2025-12-31 23:59:59'),
(UNHEX('4D79536563726574546F6B656E54776F'), 'bob@example.com', '2025-12-31 23:59:59');

INSERT INTO ResetLink (Token, Email, ExpiryTime) VALUES
('abcd1234', 'alice@example.com', '2025-12-31 23:59:59'),
('efgh5678', 'bob@example.com', '2025-12-31 23:59:59');

INSERT INTO PropertyListing (PropertyListingID,Email, Address, PostalCode, Description, Price, Bedrooms, Beds, Bathrooms, SquareMeters, ParkingSpots, Kitchens) VALUES
(20,'henry@example.com','Fjordgløtten 1, Drammen', '3041','Beautiful house with glamorous views of Drammen',2,2,2,2,175,2,1),
(21,'grace@example.com','Tangeodden 7, Steinberg','3053','Modern house close to the river in gorgeous Steinberg',2,2,2,2,185,3,1),
(22,'frank@example.com','Villaveien 3, Steinberg','3053','Comfy basement in lovely Steinberg',4,4,2,1,100,2,1),
(23,'alice@example.com','Halvorsveien 7, Steinberg','3053','Cute house in Steinberg',1,1,1,1,50,1,1);

INSERT INTO PropertyListing (PropertyListingID, Email, Address, PostalCode, Description, Price, Bedrooms, Beds, Bathrooms, SquareMeters, ParkingSpots, Kitchens) VALUES
(30, 'emma@example.com', 'Gudsgate 7, Vennesla', '10002', 'Comfy old cabin', 2, 3, 4, 2, 200, 1, 1),
(31, 'emma@example.com', 'Helvetesgate 69, Hell', '60009', 'Modern cabin by the lake', 2, 6, 9, 6, 1337, 9, 6),
(40,'alice@example.com', 'Mjogdalsvegen, Dovre', '2662', 'A lovely cabin in Dovre with a beautiful view', 2, 2, 5, 2, 100, 3, 1),
(41,'grace@example.com', 'Husabøvegen 10, Leikanger', '6863', 'Central apartment in Leikanger, renovated in 2016', 2, 1, 2, 1, 80, 1, 1),
(42,'henry@example.com', 'Smørbukkstien 6, Stavanger', '4019', 'Welcome to the ideal base in which to explore Stavanger from', 2, 1, 2, 1, 65, 1, 1),
(43,'frank@example.com', 'Kjerranveien 15, Bjørvik', '8530', 'A neat house in a neat place, perfect for people to relax and enjoy life', 2, 2, 4, 1, 90, 2, 1);


INSERT INTO PropertyListing (PropertyListingID, Email, Address, PostalCode, Description, Price, Bedrooms, Beds, Bathrooms, SquareMeters, ParkingSpots, Kitchens) VALUES
(100, 'alice@example.com', 'Strandvikvegen 553, Strandvik', '5643', 'Nice cabin in Bjørnafjord with good views of the fjord.', '2', '3', '7', '3', '220', '4', '1'),
(101, 'alice@example.com', 'Berknesvegen 222, Volda', '6105', 'Lovely vacation spot for the whole family. The property is by the sea and has a beautiful garden', '2', '3', '7', '1', '65', '1', '1'),
(102, 'alice@example.com', 'Sklibreivegen 10, Knowhere', '6975', 'Enjoy the relaxing, comforting and closed-off space Birdbox! Sleep right next to nature and its fantastic surroundings', '2', '1', '2', '1', '30', '1', '1'),
(103, 'alice@example.com', 'Soknaveien 60, Bru', '4158', 'Lovely space right by the ocean. Pier with fishing opportunities. Building and furniture made by the renowned architect Espen Surnevik', '2', '2', '3', '1', '130', '1', '1'),
(104, 'alice@example.com', 'Furnesvegen 178B, Hamar', '2319', 'Lovely and family-friendly spot ready to make memories. The area is close to a local brewery that\'s open every day', '2', '4', '8', '2', '200', '2', '1'),
(105, 'alice@example.com', 'Karsetgutua 5, Hamar', '2312', 'House on a farm that\'s in daily use. Great hiking routes. Perfect for a weekend alone or with family. Not for parties or similar events', '2', '1', '2', '1', '30', '1', '1');


INSERT INTO PropertyListing (PropertyListingID, Email, Address, PostalCode, Description, Price, Bedrooms, Beds, Bathrooms, SquareMeters, ParkingSpots, Kitchens) VALUES
(50, 'henry@example.com', 'Enebakkveien 242', '1187', 'Small house surrounded by nice landscape', 100, 2, 3, 1, 70, 1, 1),
(51, 'henry@example.com', 'Nedre Rømmesbakkan 2', '7300', 'Beautyful house close to sea', 80, 3, 3, 2, 200, 2, 1),
(52, 'henry@example.com', 'Stugguvollbekkvegen 100', '7590', 'Cozy cabin in the woods', 100, 155, 2, 3, 120, 20, 1),
(53, 'henry@example.com', 'Bjerkerudveien 25', '1450', 'Cabin with a view', 900, 1, 2, 1, 80, 2, 1);

INSERT INTO Picture (PictureID, Filename) VALUES
(100, 'listing10pic1.jpg'),
(101, 'listing10pic2.jpg'),
(102, 'listing10pic3.jpg'),
(103, 'listing10pic4.jpg'),
(104, 'listing10pic5.jpg'),
(105, 'listing11pic1.jpg'),
(106, 'listing11pic2.jpg'),
(107, 'listing11pic3.jpg'),
(108, 'listing11pic4.jpg'),
(109, 'listing11pic5.jpg'),
(110, 'listing12pic1.jpg'),
(111, 'listing12pic2.jpg'),
(112, 'listing12pic3.jpg'),
(113, 'listing12pic4.jpg'),
(114, 'listing12pic5.jpg'),
(115, 'listing13pic1.jpg'),
(116, 'listing13pic2.jpg'),
(117, 'listing13pic3.jpg'),
(118, 'listing13pic4.jpg'),
(119, 'listing13pic5.jpg'),
(120, 'listing14pic1.jpg'),
(121, 'listing14pic2.jpg'),
(122, 'listing14pic3.jpg'),
(123, 'listing14pic4.jpg'),
(124, 'listing14pic5.jpg'),
(125, 'listing15pic1.jpg'),
(126, 'listing15pic2.jpg'),
(127, 'listing15pic3.jpg'),
(128, 'listing15pic4.jpg'),
(129, 'listing15pic5.jpg');

INSERT INTO Picture (PictureID, Filename) VALUES
(50, 'Listing50pic1.jpg'),
(51, 'Listing50pic2.jpg'),
(52, 'Listing50pic3.jpg'),
(53, 'Listing50pic4.jpg'),
(54, 'Listing50Pic5.jpg'),
(55, 'Listing51pic1.jpg'),
(56, 'Listing51pic2.jpg'),
(57, 'Listing51pic3.jpg'),
(58, 'Listing51pic4.jpg'),
(59, 'Listing51pic5.jpg'),
(60, 'Listing52pic1.jpg'),
(61, 'Listing52pic2.jpg'),
(62, 'Listing52pic3.jpg'),
(63, 'Listing52pic4.jpg'),
(64, 'Listing52pic5.jpg'),
(65, 'Listing53pic1.jpg'),
(66, 'Listing53pic2.jpg'),
(67, 'Listing53pic3.jpg'),
(68, 'Listing53pic4.jpg'),
(69, 'Listing53pic5.jpg');

-- INSERT INTO Booking (PropertyListingID, Email, StartTime, EndTime) VALUES

INSERT INTO Picture (Filename) VALUES
('hus1.jpg'),
('hus2.jpg'),
('hus3.jpg'),
('hus4.jpg'),
('hus5.jpg'),
('hus6.jpg'),
('hus7.jpg'),
('hus8.jpg');

INSERT INTO Picture(PictureID,Filename) VALUES
(200,'listing20pic1.jpeg'),
(201,'listing20pic2.jpeg'),
(202,'listing20pic3.jpeg'),
(203,'listing20pic4.jpeg'),
(204,'listing20pic5.jpeg'),
(205,'listing21pic1.jpeg'),
(206,'listing21pic2.jpeg'),
(207,'listing21pic3.jpeg'),
(208,'listing21pic4.jpeg'),
(209,'listing21pic5.jpeg'),
(210,'listing22pic1.jpeg'),
(211,'listing22pic2.jpeg'),
(212,'listing22pic3.jpeg'),
(213,'listing22pic4.jpeg'),
(214,'listing22pic5.jpeg'),
(215,'listing23pic1.jpeg'),
(216,'listing23pic2.jpeg'),
(217,'listing23pic3.jpeg'),
(218,'listing23pic4.jpeg'),
(219,'listing23pic5.jpeg');
INSERT INTO Picture (PictureID, Filename) VALUES
(400,'listing40pic1.jpg'),
(401,'listing40pic2.jpg'),
(402,'listing40pic3.jpg'),
(403,'listing40pic4.jpg'),
(404,'listing40pic5.jpg'),
(405,'listing41pic1.jpg'),
(406,'listing41pic2.jpg'),
(407,'listing41pic3.jpg'),
(408,'listing41pic4.jpg'),
(409,'listing41pic5.jpg'),
(410,'listing42pic1.jpg'),
(411,'listing42pic2.jpg'),
(412,'listing42pic3.jpg'),
(413,'listing42pic4.jpg'),
(414,'listing42pic5.jpg'),
(415,'listing43pic1.jpg'),
(416,'listing43pic2.jpg'),
(417,'listing43pic3.jpg'),
(418,'listing43pic4.jpg'),
(419,'listing43pic5.jpg'),
(30, 'listing30pic1.png'),
(31, 'listing30pic2.png'),
(32, 'listing30pic3.png'),
(33, 'listing30pic4.png'),
(34, 'listing30pic5.png'),
(35, 'listing31pic1.png'),
(36, 'listing31pic2.png'),
(37, 'listing31pic3.png'),
(38, 'listing31pic4.png'),
(39, 'listing31pic5.png');

INSERT INTO PropertyPicture (PropertyListingID, PictureID) VALUES
(20,200),
(20,201),
(20,202),
(20,203),
(20,204),
(21,205),
(21,206),
(21,207),
(21,208),
(21,209),
(22,210),
(22,211),
(22,212),
(22,213),
(22,214),
(23,215),
(23,216),
(23,217),
(23,218),
(23,219);
INSERT INTO PropertyPicture (PropertyListingID, PictureID) VALUES
(40, 400),
(40, 401),
(40, 402),
(40, 403),
(40, 404),
(41, 405),
(41, 406),
(41, 407),
(41, 408),
(41, 409),
(42, 410),
(42, 411),
(42, 412),
(42, 413),
(42, 414),
(43, 415),
(43, 416),
(43, 417),
(43, 418),
(43, 419);
INSERT INTO PropertyPicture (PropertyListingID, PictureID) VALUES
(30, 30),
(30, 31),
(30, 32),
(30, 33),
(30, 34),
(31, 35),
(31, 36),
(31, 37),
(31, 38),
(31, 39);


INSERT INTO PropertyPicture (PropertyListingID, PictureID) VALUES
(100, 100),
(100, 101),
(100, 102),
(100, 103),
(100, 104),
(101, 105),
(101, 106),
(101, 107),
(101, 108),
(101, 109),
(102, 110),
(102, 111),
(102, 112),
(102, 113),
(102, 114),
(103, 115),
(103, 116),
(103, 117),
(103, 118),
(103, 119),
(104, 120),
(104, 121),
(104, 122),
(104, 123),
(104, 124),
(105, 125),
(105, 126),
(105, 127),
(105, 128),
(105, 129);
INSERT INTO PropertyPicture (PropertyListingID, PictureID) VALUES
(50, 50),
(50, 51),
(50, 52),
(50, 53),
(50, 54),
(51, 55),
(51, 56),
(51, 57),
(51, 58),
(51, 59),
(52, 60),
(52, 61),
(52, 62),
(52, 63),
(52, 64),
(53, 65),
(53, 66),
(53, 67),
(53, 68),
(53, 69);
