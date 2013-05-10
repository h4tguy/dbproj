dbproj
======

Install instructions
====================
1. Run ./setup.py in your shell
2. That's it

If you're on campus you might wanna set up your HTTP_PROXY environment variable like so:
HTTP_PROXY="hmdyas001@proxynet.uct.ac.za" ./setup.py

Database Implementation
=======================

Relations:
----------

Users (Regnum, FullName, Salt, HashedPassword, UserType)
Questions (Qno, Question, RightAnswer, SetBy, Useless, Difficulty)
MCQAns (Qno, Letter, Answer)
Answers (Regnum, Qno, Answer)
Ratings (Qno, Regnum, Points, Reason)

Explanation of Relations:
-------------------------

Users (Regnum CHAR(9) PRIMARY KEY, FullName  VARCHAR(50), Salt VARCHAR (20), HashedPassword VARCHAR(40),
 UserType VARCHAR(7)):

This provides a list of all users and details. Regnum is the user's unique identifier; salt is used as a security
measure when hashing passwords; the password stored has been hashed, and the UserType determines what privileges
the user has (student or teacher). FullName is necessary for when reporting students' results.


Questions (Qno INTEGER PRIMARY KEY, Question VARCHAR(100), RightAnswer VARCHAR(20), SetBy CHAR(9), Useless
 BOOLEAN, Difficulty INTEGER) & MCQAns (Qno INTEGER, Letter CHAR(1), Answer VARCHAR(20)):
 
All Questions, MCQ or one-word answer, are stored in Questions (Qno, Question, RightAnswer, SetBy, Useless, Difficulty). In
addition, the answers to all the MCQs are stored in MCQAns (Qno, Letter, Answer), where Letter will in general
be one of 'A','B','C' or 'D' but any MCQ is not restricted to having exactly 4 answers.


Answers (Regnum CHAR(9), Qno INTEGER, Answer VARCHAR(20)):
A table for Answers that records who answered which question with what answer.

Ratings (Qno INTEGER, Regnum CHAR(9), Points INTEGER, Reason VARCHAR(50)):
A table to store how questions were rated by users. There should be a score from 1 to 100 (points) as well as a
reason for the rating given. The rater's Regnum is also stored  should be able to safely assume no one rates
the same question twice.
