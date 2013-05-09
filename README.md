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
  returns: {'status': 1} <- 0 = failuer, 1 = student, 2 = lecturer

Get a question to answer
'/get_question':
	expects: Anything
	returns: {'question':Text of question to ask}

'/answer_question':
	expects: {'answer': answer to question}
	returns: {'correct': whether correct or not}

Get a question to rate
'/get_rate_question':
	expects: Anything
	returns: {'question': question to rate, 'answer': expected answer}

'/rate_question':
	expects: {'points': points rating, 'reason': string}
	returns: empty string

'/performance':
	expects: {'name': name of student to look up}
	returns: {'total_answered': total # qs answered, 'total_correct': total # qs correct, 'details':
	[[qno,rightanswer,answer] for all qnos answered ]}

'/questions':
	expects: {'name': value}
	returns: {'question_info':[[qno,#correct,#total,avg_rating] for qno set by name]}
	All values string formatted

'/classlist':
	expects: anything
	returns: {'classlist':[ [name,mark,avg rating of qs] for all students]}
=========================================

Checking in

Checking in - Pierre :p
