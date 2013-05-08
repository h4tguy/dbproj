
#This is a dummy class for passing metadata with questions
class Question:
	pass

def get_q(u_name,for_rating=False):
	global cur
	cur.execute('''select qno, question %s from questions where qno not in 
		(select qno from answers where regnum=%s) %s limit 1''',
		(",answer" if for_rating else "",u_name,
			''' and qno not in (select qno from answers 
			where regnum='''+str(u_name) if for_rating else ""))
	res=cur.fetchone()
	if not res:
		return None
	cur.execute('select letter,answer from mcqans where qno='+str(res[0]))
	mcq=cur.fetchall()
	ans=Question()
	ans.body=reduce(lambda x,y: str(x)+"\n"+str(y),[str(i[0])+" "+str(i[1]) for i in mcq],res[1])
	ans.qno=res[0]
	return ans

def record_q(u_name,qno,ans):
	global cur
	cur.execute('''insert into answers (regnum,qno,answer)
		values (%s,%s,%s)''',(u_name,qno,ans))
	return True

def record_rating(u_name,qno,pts,reason):
	global cur
	cur.execute('''insert into ratings (qno,regnum,points,reason)
		values (%s,%s,%s,%s)''',(qno,u_name,pts,reason))
	return True

