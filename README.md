dbproj
======

Install instructions
====================
1. Run ./setup.py in your shell
2. That's it

If you're on campus you might wanna set up your HTTP_PROXY environment variable like so:
HTTP_PROXY="hmdyas001@proxynet.uct.ac.za" ./setup.py

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

'/score_questions':
	expects: anything
	returns: {'diff_data':[[int qno,str question, str ans, str diff]for all questions]}

'/check_weak_questions':
	expects: anything
	returns: {'questions':[[int qno, str question, str ans, bool useless ] for questions with difficulty=3]}

'/update_weak_questions':
	expects: {'trues':[qnos which must be made useless], 'falses':[qnos which must be unmade
	useless]}
	returns: empty string

'/make_test':
	expects: anything
	returns: {'questions':[str questions], 'answers':[str answers]}
	There will be at most ten questions and at most 10 anses, and there will be the same # of each


=========================================
Checking in

Checking in - Pierre :p
