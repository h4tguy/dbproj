#Data on students, for use by staff
from flask import g

class Info:
	pass

def cust_fmt(x):
	if x<0:
		return "n/a"
	return "%.2f"%(x)
def perc_fmt(x):
	if x<0:
		return "n/a"
	return "%.2f%%"%(100*x)

def answer_info(u_name):
	cur = g.db.cursor()
	cur.execute('''select questions.qno,rightanswer,answer from
	questions inner join answers on questions.qno=answers.qno
	where answers.regnum=%s''',(u_name,))
	res=cur.fetchall()
	cur.execute('select fullname from users where regnum=%s',(u_name,))
	nm=cur.fetchone()[0]
	cur.close()
	corr=[1 if i[1]==i[2] else 0 for i in res]
	ans=Info()
	ans.answered=len(res)
	ans.correct=sum(corr)
	ans.detail=res
	ans.name=nm
	return ans

def question_info(u_name):
	cur = g.db.cursor()
	res=dict()
	cur.execute('select distinct qno,question from questions where setby=%s',(u_name,))
	for i in cur.fetchall():
		res[i[0]]=Info()
		res[i[0]].corr=0
		res[i[0]].tot=0
		res[i[0]].rat=0
		res[i[0]].qtxt=i[1]
	cur.execute('''select questions.qno,count(*) from questions inner join answers
	on questions.qno=answers.qno and rightanswer=answer
	where questions.setby=%s group by questions.qno''',(u_name,))
	corr=cur.fetchall()
	for i in corr:
		if i[0] in res:
			res[i[0]].corr=i[1]
	cur.execute('''select questions.qno,count(*) from questions inner join answers
	on questions.qno=answers.qno
	where questions.setby=%s group by questions.qno''',(u_name,))
	tot=cur.fetchall()
	for i in tot:
		if i[0] in res:
			res[i[0]].tot=i[1]
	cur.execute('''select questions.qno,avg(points) from questions inner join ratings
	on questions.qno=ratings.qno
	where questions.setby=%s group by questions.qno''',(u_name,))
	rat=cur.fetchall()
	for i in rat:
		if i[0] in res:
			res[i[0]].rat=i[1]
	ans=[]
	ans=[{'qid':str(i),'question':str(res[i].qtxt),'correct':str(res[i].corr),'incorrect':str(res[i].tot-res[i].corr),'rating':cust_fmt(res[i].rat)} for i in res]
	cur.close()
	return ans

def get_classlist():
	cur = g.db.cursor()
	cur.execute('''select regnum from Users where usertype='1' ''')
	names=[i[0] for i in cur.fetchall()]
	res=dict()
	for i in names:
		res[i]=Info()
		res[i].qs=-1
		res[i].ans=-1
	cur.execute('''select setby, avg(points) from questions inner join ratings
	on questions.qno=ratings.qno
	group by setby''')
	qs=cur.fetchall()
	cur.execute('''select regnum, avg((rightanswer=answer)::int) from questions inner join
	answers on questions.qno=answers.qno group by regnum''')
	anss=cur.fetchall()
	for i in anss:
		if i[0] in res:
			res[i[0]].ans=i[1]
	for i in qs:
		if i[0] in res:
			res[i[0]].qs=i[1]
	ans=[(i,perc_fmt(100*res[i].ans),cust_fmt(res[i].qs)) for i in res]
	ans.sort()
	cur.close()
	return ans




