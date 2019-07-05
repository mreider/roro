USE roro;
CREATE TABLE IF NOT EXISTS 'user' (
	'id'	INTEGER PRIMARY KEY AUTOINCREMENT,
	'first_name'	TEXT,
	'last_name'	TEXT,
	'image'	TEXT
);
CREATE TABLE IF NOT EXISTS 'message' (
	'id'	INTEGER PRIMARY KEY AUTOINCREMENT,
	'user_id'	INTEGER,
	'body'	TEXT,
	'date'	TEXT
);
INSERT INTO 'user' VALUES (1,'Matt','Reider
','matt.jpeg');
INSERT INTO 'user' VALUES (2,'Suzie','Reider
','suzie.jpeg');
INSERT INTO 'user' VALUES (3,'Jacob','Reider','jacob.jpeg');
INSERT INTO 'user' VALUES (4,'janet','Reider','janet.jpeg');
INSERT INTO 'user' VALUES (5,'Juliet','Sampson','juliet.jpeg');
INSERT INTO 'user' VALUES (6,'Simon','Mays-Smith','simon.jpeg');
INSERT INTO 'user' VALUES (7,'Charlotte','Reider-Smith','charlotte.jpeg');
INSERT INTO 'user' VALUES (8,'Rosie','Reider-Smith','rosie.jpeg');
INSERT INTO 'user' VALUES (9,'Zach','Cutburth','zach.jpeg');
INSERT INTO 'user' VALUES (10,'Molly','Reider','molly.jpeg');
INSERT INTO 'user' VALUES (11,'Brandon','Lafayette','brandon.jpeg');
INSERT INTO 'user' VALUES (12,'Deborah','Green','deb.jpeg');
INSERT INTO 'user' VALUES (13,'Bobby','Bruce','bobby.jpeg');
INSERT INTO 'user' VALUES (14,'Yank','Eppinger','yank.jpeg');
INSERT INTO 'user' VALUES (15,'Barby','Eppinger','barby.jpeg');
INSERT INTO 'user' VALUES (16,'Caleb','Banta-Green','caleb.jpeg');
INSERT INTO 'user' VALUES (17,'Kate','Banta-Green','kate.jpeg');
INSERT INTO 'user' VALUES (18,'Isaac','Mays-Smith','isaac.jpeg');
INSERT INTO 'user' VALUES (19,'Tom','Frankel','tom.jpeg');
INSERT INTO 'user' VALUES (20,'Ellen','Frankel','ellen.jpeg');
INSERT INTO 'user' VALUES (21,'Alison','Cohen','alison.jpeg');
INSERT INTO 'user' VALUES (22,'John','Sampson Jr','johnjr.jpeg');
INSERT INTO 'user' VALUES (23,'John','Sampson Sr','johnsr.jpeg');
INSERT INTO 'user' VALUES (24,'Sharon','Litsky','sharon.jpeg');
INSERT INTO 'user' VALUES (25,'Sam','Reider','sam.jpeg');
INSERT INTO 'user' VALUES (27,'Alicia','Oullette','alicia.jpeg');
INSERT INTO 'user' VALUES (28,'Kathryn','Sheller','kathryn.jpeg');
COMMIT;
