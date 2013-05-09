#Data on students, for use by staff

class Info:
	pass

def answer_info(u_name):
	global cur
	cur.execute('''select qno,rightanswer,answer from 
	questions inner join answers on questions.qno=answers.qno
	where answers.regnum=%s''',(u_name,))
	res=cur.fetchall()
	corr=[1 if i[1]==i[2] else 0 for i in res]
	ans=Info()
	ans.answered=res.size()
	ans.correct=sum(corr)
	ans.detail=res
	return ans

def answer_info(u_name):
	global cur
	res=dict()
	cur.execute('select distinct qno from questions where setby=%s',(u_name,))
	for i in curr.fetchall():
		res[i[0]]=Info()
		res[i[0]].corr=0
		res[i[0]].tot=0
		res[i[0]].rat=0
	cur.execute('''select qno,count(*) from questions inner join answers
	on questions.qno=answers.qno and rightanswer=answer 
	where questions.setby=%s group by qno''',(u_name,))
	corr=cur.fetchall()
	for i in corr:
		if i[0] in res:
			res[i[0]].corr=i[1]
	cur.execute('''select qno,count(*) from questions inner join answers
	on questions.qno=answers.qno 
	where questions.setby=%s group by qno''',(u_name,))
	tot=cur.fetchall()
	for i in tot:
		if i[0] in res:
			res[i[0]].tot=i[1]
	cur.execute('''select qno,avg(points) from questions inner join ratings
	on questions.qno=rating.qno 
	where questions.setby=%s group by qno''',(u_name,))
	rat=cur.fetchall()
	for i in rat:
		if i[0] in res:
			res[i[0]].rat=i[1]
	ans=[]
	ans=[(i,i.corr,i.tot,i.rat) for i in res]
	return ans




