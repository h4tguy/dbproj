dbproj
======

Required packages to run web server:
	Flask (web framework)
	Psycopg (postgresql driver)

=========================================
JSON API
=========================================
'/get_salt':
  expects: {'studentno': value}
  returns: {'studentno': value, 'salt': salt_value, 'temp_salt': temp_salt_value}

'/login':
  expects: {'studentno': value, 'hash': hashed_string}
  returns: {'status': boolean} <- lowercase 'true' or 'false'

'/answer_question':
  expects: {qid: '34', answer: 'answer'},
  returns: {iscorrect: 1} <- 1 = true, 0 = false

'/get_question':
  expects: {current_qid: '34'}
  returns: 
    {qid: '35', type: 'WordQ', question: 'new question?'}
    OR
    {qid: '35', type: 'MCQ', question: 'new question?' A: 'option a', B: 'option b', C: 'option c', D: 'option d'}
NOTE: The very first question HAS to be a WordQ or the system will break a little bit.

'/rate_question':
  expects: {qid: '56', rating: '23', reason: 'its l33t'}
  returns nothing

'/performance/student_number'
  returns: {name: 'Jonathan Davis', correct: '45', incorrect: '179', grade: '0.17'}

'/check_weak_question'
 expects: {studentno: 'DBRJAR001'}
 returns: 

 (this is a json object with one key - 'questions' - which contains a list of the questions they've generated):

{
  questions: [{
    qid: '76',
    name: 'Question One',
    correct: '4',
    incorrect: '743',
    grade: '0.98'  
  }, {
    name: 'Question Two',
    correct: '11',
    incorrect: '523',
    grade: '0.23'  
  }, {
    name: 'Question Three',
    correct: '45',
    incorrect: '179',
    grade: '0.7'  
  }, {
    name: 'Question Four',
    correct: '73',
    incorrect: '34',
    grade: '0.65'  
  }]
}

=========================================

Checking in

Checking in - Pierre :p
