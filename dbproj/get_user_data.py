#Data on students, for use by staff

class Info:
	pass

def question_info(u_name):
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





