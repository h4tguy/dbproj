from flask import g

#This is a dummy class for passing metadata with questions
class Question:
	pass

def get_q_type(qid

def get_q(username, for_rating=False):
	cur = g.db.cursor()

	if for_rating:
		cur.execute('''select qno, question, rightanswer  from questions where qno not in
			(select qno from answers where regnum=%s)  and qno not in (select qno from answers
				where regnum=%s limit 1''',(username,username))
	else:
		cur.execute('''select qno, question, rightanswer  from questions where qno not in
			(select qno from answers where regnum=%s) limit 1''',
			(username, ))

	res=cur.fetchone()
	if not res:
		return None

	cur.execute('select letter,answer from mcqans where qno='+str(res[0]))
	mcq=cur.fetchall()
	cur.close()


	ans=Question()
	ans.ans=res[2]
	ans.body=reduce(lambda x,y: str(x)+"\n"+str(y),[str(i[0])+" "+str(i[1]) for i in mcq],res[1])
	ans.qno=int(res[0])

	return ans

def record_ans(u_name,qno,ans):
	global cur
	cur.execute('''insert into answers (regnum,qno,answer)
		values (%s,%s,%s)''',(u_name,qno,ans))
	return True

def record_rating(u_name,qno,pts,reason):
	global cur
	cur.execute('''insert into ratings (qno,regnum,points,reason)
		values (%s,%s,%s,%s)''',(qno,u_name,pts,reason))
	return True

