from dbproj.db import connect_database

sql = '''CREATE TABLE IF NOT EXISTS Users (
	Regnum VARCHAR(9) PRIMARY KEY,
	FullName VARCHAR(50) NOT NULL,
	Salt VARCHAR (20) NOT NULL,
	HashedPassword VARCHAR(40),
	UserType VARCHAR(7) NOT NULL
);

CREATE TABLE IF NOT EXISTS Questions (
	Qno INTEGER PRIMARY KEY,
	Question VARCHAR(100) NOT NULL,
	RightAnswer VARCHAR(20) NOT NULL,
	SetBy VARCHAR(9) NOT NULL,
	Useless BOOLEAN
);

CREATE TABLE IF NOT EXISTS MCQans (
	Qno INTEGER REFERENCES Questions (Qno),
	Letter VARCHAR(1) NOT NULL,
	Answer VARCHAR(20) NOT NULL,

	PRIMARY KEY( Qno, Letter )
);

CREATE TABLE IF NOT EXISTS Answers (
	Regnum VARCHAR(9) REFERENCES Users (Regnum),
	Qno INTEGER REFERENCES Questions (Qno),
	Answer VARCHAR(20),

	PRIMARY KEY( Regnum, Qno )
);

CREATE TABLE IF NOT EXISTS Ratings (
	Qno INTEGER REFERENCES Questions (Qno),
	Regnum VARCHAR(9) REFERENCES Users (Regnum),
	Points INTEGER,
	Reason VARCHAR(50),

	PRIMARY KEY( Qno, Regnum )
);

CREATE TABLE IF NOT EXISTS QuestionDifficulty (
	Qno INTEGER PRIMARY KEY REFERENCES Questions (Qno),
	Difficulty VARCHAR(8)
);'''

db = connect_database()
c = db.cursor()
c.execute(sql)
c.close()
db.commit()
print 'yes?'
