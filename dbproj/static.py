from flask import render_template
from dbproj import app

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
