class Difficulty:
	diffs=['Easy','Medium','Difficulty','Unusable']
	def get(x):
		return diffs[x]
def update_scores():
	global cur
	cur.execute('''update questions inner join (select qno,avg((rightanswer=answer)::int) as ans_rate
	from questions inner join answers on questions.qno=answers.qno group by qno)
	set difficulty=2 where ans_rate>0.05''') 
	cur.execute('''update questions inner join (select qno,avg((rightanswer=answer)::int) as ans_rate
	from questions inner join answers on questions.qno=answers.qno group by qno)
	set difficulty=1 where ans_rate>0.25''') 
	cur.execute('''update questions inner join (select qno,avg((rightanswer=answer)::int) as ans_rate
	from questions inner join answers on questions.qno=answers.qno group by qno)
	set difficulty=0 where ans_rate>0.75''') 
	return True

def score_questions():
	update_scores()
	cur.execute('''select qno, question, rightanswer,difficulty from question''')
	questions=cur.fetchall()
	cur.execute('select qno,letter,answer from mcqans order by letter')
	anses=cur.fetchall()
	qdict=dict()
	for i in questions:
		qdict[i[0]]=i[1:4]
	for i in anses:
		qdict[i[0]][1]=qdict[i[0]][1]+" "+i[1]+") "+i[2]
	return [[i]+qdict[i] for i in qdict]
	

def check_weak_questions():
	update_scores()
	pass

def gen_test():
	update_scores()
	ans=[]
