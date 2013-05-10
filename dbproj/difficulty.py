from flask import g
class Difficulty:
	#In the questions relation, difficulty is stored as a number from 0 to 3, which represent the following words:
	diffs=['Easy','Average','Hard','Unusable']
	def get(x):
		return diffs[x]
#Method to set the difficulty for every question
def update_scores():
	#Get the average number of times a question was correctly answered for every question. Use this average to determine how hard it is
	cur = g.db.cursor()
	cur.execute('select qno from questions')
	res = cur.fetchall()
	for question in res:
		ans_rate_cursor = g.db.cursor()
		ans_rate_cursor.execute('select avg((rightanswer=answer)::int) as ans_rate from questions inner join answers on questions.qno=answers.qno where questions.qno = %s', (question[0], ))
		ans_rate = ans_rate_cursor.fetchone()[0]
		ans_rate_cursor.close()

		difficulty = None
		if ans_rate > 0.75:
			difficulty = 0
		elif ans_rate > 0.25:
			difficulty = 1
		elif ans_rate > 0.05:
			difficulty = 2
		else:
			difficulty = 3

		#Check if the average rating was 1, in which case the question will be marked unsuable
		cur.execute('select avg(points) as score from ratings where qno = %s', (question, ))
		score = cur.fetchone()[0]
		if score < 2:
			difficulty = 3

		cur.execute('update questions set difficulty = %s where qno = %s', (difficulty, question))


		g.db.commit()

	#Also set any question to unusable if a staff member has flagged it useless
	cur.execute('''update questions
	set difficulty=3 where useless''')
	cur.close()
	g.db.commit()

	return True

#Method that gets all the questions and their details to let them be rated
def score_questions():
	update_scores()
	cur = g.db.cursor()
	cur.execute('''select qno, question, rightanswer,difficulty from questions''')
	questions=cur.fetchall()
	cur.execute('select qno,letter,answer from mcqans order by letter')
	anses=cur.fetchall()
	cur.close()
	qdict=dict()
	for i in questions:
		qdict[i[0]]=list(i[1:4])
		qdict[i[0]][2]=Difficulty.diffs[i[3]]
	for i in anses:
		qdict[i[0]][0]=qdict[i[0]][0]+" "+i[1]+") "+i[2]
	return [{'qno':i,'question':qdict[i][0],'rightans':qdict[i][1],'difficulty':qdict[i][2]} for i in qdict]

#Method to get 'weak' questions so that a staff member can examine them and flag some unusable
def check_weak_questions():
	update_scores()
	cur = g.db.cursor()
	#Get weak questions and their details
	cur.execute('''select qno,question, rightanswer,useless from questions where difficulty=3''')
	res=cur.fetchall()
	#If the questions are MCQs, their answers will also be retrieved for examination
	cur.execute('''select mcqans.qno,letter,answer from questions inner join mcqans	on mcqans.qno=questions.qno where difficulty=3''')
	anses=cur.fetchall()
	qs=dict()
	#Match MCQ answers with their questions and format everything suitable to return
	for i in res:
		qs[i[0]]=list(i[1:4])
	for i in anses:
		qs[i[0]][0]+=" "+i[1]+") "+i[2]
	cur.close()
	return [{'qno':i,'question':qs[i][0],'rightans':qs[i][1],'useless':qs[i][2]} for i in qs]

def sqlify(x):
	if len(x)==0:
		return ""
	if len(x)==1:
		return "(%s)"%x[0]
	return str(tuple(map(int,x)))

#Method that updates the database to flag the questions the staff member wants flagged as useless
def update_weak_question(trues, falses):
	print trues,falses
	trues=sqlify(trues)
	falses=sqlify(falses)
	cur = g.db.cursor()
	if len(trues)>0:
		cur.execute('''update questions set useless=true where qno in %s'''% trues)
	if len(falses)>0:
		cur.execute('''update questions set useless=false where qno in %s'''%falses)
	cur.close()
	g.db.commit()
	return True

#Method that generates a test of up to 10 questions that vary in difficulty levels
def gen_test():
	cur = g.db.cursor()
	update_scores()
	cur.execute('''select qno,question, rightanswer from questions where difficulty=0 limit 3''')
	qs=[list(x) for x in cur.fetchall()]
	cur.execute('''select qno, question, rightanswer from questions where difficulty=1 limit 4''')
	qs=qs+[list(x) for x in cur.fetchall()]
	cur.execute('''select qno, question, rightanswer from questions where difficulty=2 limit 3''')
	qs=qs+[list(x) for x in cur.fetchall()]
	qs = list(qs)
	#Need to get MCQs answers and match them to the questions
	qnos=[i[0] for i in qs]
	cur.execute('''select qno,letter,answer from mcqans
			where qno in %s order by letter'''%str(tuple(qnos)))
	anses=cur.fetchall()
	cur.close()
	for i in xrange(len(qs)):
		for j in anses:
			if qs[i][0]==j[0]:
				qs[i][1]+=" "+j[1]+") "+j[2]
				break
	return[{'question':i[1],'answer':i[2]} for i in qs]
