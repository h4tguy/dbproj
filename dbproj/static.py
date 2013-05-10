from flask import render_template
from dbproj import app

@app.route('/menu/student')
def menuStudent():
	return render_template('menuStudent.html')

@app.route('/menu/teacher')
def menuStudent():
	return render_template('menuTeacher.html')

@app.route('/questions/answer')
def answerQuestions():
	return render_template('answerQuestions.html')

@app.route('/questions/rate')
def rateQuestions():
	return render_template('rateQuestions.html')
