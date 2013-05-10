from flask import g
class Difficulty:
	diffs=['Easy','Average','Hard','Unusable']
	def get(x):
		return diffs[x]
def update_scores():
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

		cur.execute('select avg(points) as score from ratings where qno = %s', (question, ))
		score = cur.fetchone()[0]
		if score < 2:
			difficulty = 3

		cur.execute('update questions set difficulty = %s where qno = %s', (difficulty, question))


		g.db.commit()


	cur.execute('''update questions
	set difficulty=3 where useless''')
	cur.close()
	g.db.commit()

	return True

def score_questions():
	update_scores()
	c = g.db.cursor()
	cur.execute('''select qno, question, rightanswer,difficulty from questions''')
	questions=cur.fetchall()
	cur.execute('select qno,letter,answer from mcqans order by letter')
	anses=cur.fetchall()
	c.close()
	qdict=dict()
	for i in questions:
		qdict[i[0]]=i[1:4]
		qdict[i[0]][2]=Difficulty.get(i[3])
	for i in anses:
		qdict[i[0]][0]=qdict[i[0]][0]+" "+i[1]+") "+i[2]
	return [[i]+qdict[i] for i in qdict]


def check_weak_questions():
	update_scores()
	cur = g.db.cursor()
	cur.execute('''select qno,question, rightanswer,useless from questions where difficulty=3''')
	res=cur.fetchall()
	cur.execute('''select mcqans.qno,letter,answer from questions inner join mcqans	on mcqans.qno=questions.qno where difficulty=3''')
	anses=cur.fetchall()
	qs=dict()
	for i in res:
		qs[i[0]]=i[1:4]
		qs[i[0]][2]=int(qs[i[0]][2])
	for i in anses:
		qs[i[0]][0]+=" "+i[1]+") "+i[2]
	cur.close()
	return [[i]+qs[i] for i in qdict]

def update_weak_question(trues, falses):
	trues=tuple(trues)
	falses=tuple(falses)
	cur = g.db.cursor()
	cur.execute('''update questions set useless=true where qno in %s'''% str(trues))
	cur.execute('''update questions set useless=false where qno in %s'''%str(falses))
	cur.close()
	g.db.commit()
	return True

def gen_test():
	cur = g.db.cursor()
	update_scores()
	cur.execute('''select qno,question, rightanswer from questions where difficulty=0 limit 3''')
	qs=cur.fetchall()
	cur.execute('''select qno, question, rightanswer from questions where difficulty=1 limit 4''')
	qs=qs+cur.fetchall()
	cur.execute('''select qno, question, rightanswer from questions where difficulty=2 limit 3''')
	qs=qs+cur.fetchall()
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
