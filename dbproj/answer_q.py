from flask import g

#This is a dummy class for passing metadata with questions
class Question:
	qno = None
	ans = None
	body = None
	qtype = None

#Get whether a question is an MCQ or not
def get_q_type(qid):
	cur = g.db.cursor()

	cur.execute('select count(*) from mcqans where qno = %s', (qid, ))
	questionType = 'MCQ' if cur.fetchone()[0] > 0 else 'WordQ'
	cur.close()

	return questionType

#Get the next question to ask a user
def get_q(username, for_rating=False):
	cur = g.db.cursor()

	if not for_rating: #ie. if the question is not being retrieved to let the user rate the question, but rather to answer it
		cur.execute('''select qno, question, rightanswer  from questions where qno not in
			(select qno from answers where regnum=%s)  and qno not in (select qno from ratings
				where regnum=%s) and not useless limit 1''',(username,username))
		# This query gets 1 question that the answer has not yet answered or rated yet and is not flagged useless
	else: #If the question is for rating, then check that the user hasn't yet rated it
		cur.execute('''select qno, question, rightanswer  from questions where qno not in
			(select qno from ratings where regnum=%s) and not useless limit 1''',
			(username, ))

	res=cur.fetchone()
	if not res:
		return None
	#If the question is an MCQ, the answers are required:
	cur.execute('select letter,answer from mcqans where qno='+str(res[0]))
	mcq=cur.fetchall()
	cur.close()

	#ans is the object that will be returned containing all the data
	ans=Question()
	ans.ans=res[2]
	ans.body = res[1]
	ans.qno = int(res[0])
	ans.qtype = get_q_type(ans.qno)

	ans.mcq = dict((x[0], x[1]) for x in mcq)

	return ans

#Records a student's answer to a question in the answers table
def record_ans(u_name,qno,ans):
	cur = g.db.cursor()
	cur.execute('''insert into answers (regnum,qno,answer)
		values (%s,%s,%s)''',(u_name,qno,ans))
	cur.close()
	g.db.commit()
	return True
#Records a rating of a question
def record_rating(u_name,qno,pts,reason):
    if pts > 100:
        return False
	cur = g.db.cursor()
	cur.execute('''insert into ratings (qno,regnum,points,reason)
		values (%s,%s,%s,%s)''',(qno,u_name,pts,reason))
	cur.close()
	g.db.commit()

	return True

