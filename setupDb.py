from dbproj.db import connect_database

sql = '''CREATE TABLE IF NOT EXISTS Users (
	Regnum CHAR(9) PRIMARY KEY,
	FullName VARCHAR(50) NOT NULL,
	Salt VARCHAR (20) NOT NULL,
	HashedPassword VARCHAR(40),
	UserType VARCHAR(7) NOT NULL
);

CREATE TABLE IF NOT EXISTS Questions (
	Qno INTEGER PRIMARY KEY,
	Question VARCHAR(100) NOT NULL,
	RightAnswer VARCHAR(20) NOT NULL,
	SetBy CHAR(9) NOT NULL,
	Useless BOOLEAN,
	Difficulty INTEGER CONSTRAINT ValidDifficulty CHECK (Difficulty >=0 AND Difficulty <= 3))
);

CREATE TABLE IF NOT EXISTS MCQans (
	Qno INTEGER REFERENCES Questions (Qno),
	Letter CHAR(1) NOT NULL,
	Answer VARCHAR(20) NOT NULL,

	PRIMARY KEY( Qno, Letter )
);

CREATE TABLE IF NOT EXISTS Answers (
	Regnum CHAR(9) REFERENCES Users (Regnum),
	Qno INTEGER REFERENCES Questions (Qno),
	Answer VARCHAR(20),

	PRIMARY KEY( Regnum, Qno )
);

CREATE TABLE IF NOT EXISTS Ratings (
	Qno INTEGER REFERENCES Questions (Qno),
	Regnum CHAR(9) REFERENCES Users (Regnum),
	Points INTEGER CONSTRAINT ValidRatingScore CHECK (Points <= 100 AND Points > 0),
	Reason VARCHAR(50),

	PRIMARY KEY( Qno, Regnum )
);'''

db = connect_database()
c = db.cursor()
c.execute(sql)
c.close()
db.commit()
print 'yes?'
