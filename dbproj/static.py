from flask import render_template
from dbproj import app, answer_q

@app.route('/menuStudent')
def menuStudent():
	return render_template('menuStudent.html')

@app.route('/menuTeacher')
def menuTeacher():
	return render_template('menuTeacher.html')

@app.route('/questionsAnswer')
def answerQuestions():
	return render_template('answerQuestions.html')

@app.route('/questionsRate')
def rateQuestions():
	return render_template('rateQuestions.html')

@app.route('/checkStudentAnswers')
def checkStudentAnswers():
	return render_template('checkStudentAnswers.html')

@app.route('/checkStudentQuestions')
def checkStudentQuestions():
	return render_template('checkStudentQuestions.html')

@app.route('/view_classlist')
def view_classlist():
	return render_template('classList.html')
