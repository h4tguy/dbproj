class Difficulty:
	diffs=['Easy','Medium','Difficulty','Unusable']
	def get(x):
		return diffs[x]
def update_scores():
	global cur
	cur.execute('''update questions inner join (select qno,avg((rightanswer=answer)::int) as ans_rate
	from questions inner join answers on questions.qno=answers.qno group by qno)
	set difficulty=3 ''') 
	cur.execute('''update questions inner join (select qno,avg((rightanswer=answer)::int) as ans_rate
	from questions inner join answers on questions.qno=answers.qno group by qno)
	set difficulty=2 where ans_rate>0.05''') 
	cur.execute('''update questions inner join (select qno,avg((rightanswer=answer)::int) as ans_rate
	from questions inner join answers on questions.qno=answers.qno group by qno)
	set difficulty=1 where ans_rate>0.25''') 
	cur.execute('''update questions inner join (select qno,avg((rightanswer=answer)::int) as ans_rate
	from questions inner join answers on questions.qno=answers.qno group by qno)
	set difficulty=0 where ans_rate>0.75''') 
	cur.execute('''update questions inner join (select qno,avg(points) as score 
	from questions inner join ratings on questions.qno=ratings.qno group by qno)
	set difficulty=3 where score<2''') 
	cur.execute('''update questions 
	set difficulty=3 where useless''') 

	return True

def score_questions():
	update_scores()
	cur.execute('''select qno, question, rightanswer,difficulty from questions''')
	questions=cur.fetchall()
	cur.execute('select qno,letter,answer from mcqans order by letter')
	anses=cur.fetchall()
	qdict=dict()
	for i in questions:
		qdict[i[0]]=i[1:4]
		qdict[i[0]][2]=Difficulty.get(i[3])
	for i in anses:
		qdict[i[0]][0]=qdict[i[0]][0]+" "+i[1]+") "+i[2]
	return [[i]+qdict[i] for i in qdict]
	

def check_weak_questions():
	update_scores()
	cur.execute('''select qno,question, rightanswer,useless from questions where difficulty=3''')
	res=cur.fetchall()
	cur.execute('''select mcqans.qno,letter,answer from questions inner join mcqans
	on mcqans.qno=questions.qno where difficulty=3''')
	anses=cur.fetchall()
	qs=dict()
	for i in res:
		qs[i[0]]=i[1:4]
		qs[i[0]][2]=int(qs[i[0]][2])
	for i in anses:
		qs[i[0]][0]+=" "+i[1]+") "+i[2]
	return [[i]+qs[i] for i in qdict]

def update_weak_question(trues, falses):
	trues=tuple(trues)
	falses=tuple(falses)
	cur.execute('''update questions set useless=true where qno in %s''',(str(trues),))
	cur.execute('''update questions set useless=false where qno in %s''',(str(falses),))
	return True

def gen_test():
	update_scores()
	cur.execute('''select qno,question, rightanswer from questions where difficulty=0 limit 3''')
	qs=cur.fetchall()
	cur.execute('''select qno, question, rightanswer from questions where difficulty=1 limit 4''')
	qs=qs+cur.fetchall()
	cur.execute('''select qno, question, rightanswer from questions where difficulty=2 limit 3''')
	qs=qs+cur.fetchall()
	qnos=[i[0] for i in qs]
	cur.execute('''select qno,letter,answer from mcqans
			where qno in %s order by letter''', (str(tuple(qnos)),))
	anses=cur.fetchall()
	for i in xrange(len(qs)):
		for j in anses:
			if qs[i][0]==j[0]:
				qs[i][1]+=" "+j[1]+") "+j[2]
				break
	return[[i[0] for i in qs],[i[1] for i in qs]]
