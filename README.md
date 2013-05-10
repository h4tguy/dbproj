dbproj
======

Install instructions
====================
1. Run ./setup.py in your shell
2. That's it

If you're on campus you might want to set up your HTTP_PROXY environment variable like this:
HTTP_PROXY="hmdyas001@proxynet.uct.ac.za" ./setup.py

Description
=======================

This app tests students using student-submitted questions, and reports back students' performance.

Users are able to register accounts and log in. Once logged in, they are displayed a menu:

Students only have permissions to answer questions and to rate questions (ie. indicate how suitable a question is for
usage). If they opt to answer questions, they are shown questions (both MCQ and One-Word-Answers (OWA)) to answer.
They are not shown questions they have already answered. They are also able to give any questions a score from 1 to 100
along with a reason for their rating. Students can also navigate back to the main menu at any point.

Teachers are able to view a class list, reporting back the results of all the students (in terms of how well they did at
answering questions). They can also view all 'weak' questions - questions which no one answered correctly or that were 
rated very poorly. They can flag these weak questions as unusable, in which case they will not be asked in the future. 
They can also view a report on all the questions that have been submitted, check a specific students' performance at 
answering questions, and check a specific students' questions. Teachers are also given the ability to generate a test 
of up to 10 questions, with a certain number of questions of varying levels of difficulty.

Database Implementation
=======================

Relations:
----------

Users (Regnum CHAR(9) PRIMARY KEY, FullName  VARCHAR(50), Salt VARCHAR (20), HashedPassword VARCHAR(40),
 UserType VARCHAR(7))


Questions (Qno INTEGER PRIMARY KEY, Question VARCHAR(100), RightAnswer VARCHAR(20), SetBy CHAR(9), Useless
 BOOLEAN, Difficulty INTEGER)


MCQAns (Qno INTEGER, Letter CHAR(1), Answer VARCHAR(20))


Answers (Regnum CHAR(9), Qno INTEGER, Answer VARCHAR(20))


Ratings (Qno INTEGER, Regnum CHAR(9), Points INTEGER, Reason VARCHAR(50))


Explanation of Relations:
-------------------------

Users (Regnum, FullName, Salt, HashedPassword, UserType):
This provides a list of all users and details. Regnum is the user's unique identifier; salt is used as a security
measure when hashing passwords; the password stored has been hashed, and the UserType determines what privileges
the user has (student or teacher). FullName is necessary for when reporting students' results.


Questions (Qno, Question, RightAnswer, SetBy, Useless, Difficulty) & MCQAns (Qno, Letter, Answer): 
All Questions, MCQ or one-word answer, are stored in Questions (Qno, Question, RightAnswer, SetBy, Useless, Difficulty). In
addition, the answers to all the MCQs are stored in MCQAns (Qno, Letter, Answer), where Letter will in general
be one of 'A','B','C' or 'D' but any MCQ is not restricted to having exactly 4 answers.


Answers (Regnum, Qno, Answer):
A table for Answers that records who answered which question with what answer.

Ratings (Qno, Regnum, Points, Reason):
A table to store how questions were rated by users. There should be a score from 1 to 100 (points) as well as a
reason for the rating given. The rater's Regnum is also stored  should be able to safely assume no one rates
the same question twice.

Database Interaction
====================

setupDb.py contains the commands that create the database.

db.py returns a connection to the database.

authentication.py handles database queries required for login and finds the User Type to check if the role of the user 
in the system has permissions for access.

answer_q.py handles all the interaction necessary for allowing a student to answer a question. This includes getting the 
question, getting the possible answers for MCQs, and recording the student's answer.

get_user_data.py handles the interaction for reports about a specific student or the whole class list.

difficulty.py handles setting the difficulty of questions, handling 'weak' questions and generates a test of up to 10 
questions, varying in difficulty.

List of Files
=============

AnswerData.csv

MCQAnsData.csv

QuestionsData.csv

README.md

ratingsData.csv

requirements.txt

runInVenv.sh

runserver.py

setup.sh

setupDb.py

userlist.csv

dbproj:

  __init__.py
  
  answer_q.py
  
  authentication.py
  
  config.py
  
  db.py
  
  difficulty.py
  
  get_user_data.py
  
  static.py
  
  templates:
  
    answerQuestionPage.html
    
    checkStudentAnswers.html
    
    checkStudentQuestions.html
    
    classList.html
    
    generateTest.html
    
    index.html
    
    menu.html
    
    menuStudent.html
    
    rateQuestions.html
    
  static: 
  
    css:
    
       app.css
       
       base.css
       
    img:
    
       bg.png
       
       logo-icon.png
       
    js:
    
       app.js
       
       jquery.js
       
       md5.js
