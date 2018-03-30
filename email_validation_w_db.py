from flask import Flask, render_template, request, redirect, flash, session
import re
from mysqlconnection import MySQLConnector

# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
mysql = MySQLConnector(app, 'email_validation')

app.secret_key = "unicorns"

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
	validate = "SELECT * FROM emails"
	emails = mysql.query_db(validate)
	# iterate through query of all emails
	for email in emails:
		# check if email from emails is equal to the list value: 'email'
		if email['email'] == request.form['email']:
			flash("Email Address already exists! Try being original for once, thanks!")
			return redirect('/')

	if not EMAIL_REGEX.match(request.form['email']):
		flash("Invalid Email Address!")
		return redirect('/')
	else:
		flash("Success! Thanks for submitting your information!")
		query = "INSERT INTO emails (email, created_at) VALUES (:email, NOW())"
		data = { 'email': request.form['email'] }
		mysql.query_db(query, data)
		return redirect('/success')
		
@app.route('/success')
def success():
	query = "SELECT * FROM emails"
	emails = mysql.query_db(query)
	print emails
	return render_template('success.html', emails=emails)

@app.route('/remove', methods=["POST"])
def remove():
	query = "DELETE FROM emails WHERE id = :id"
	data = { 'id': request.form['friend_id']}
	mysql.query_db(query, data)
	return redirect('/success')
	
app.run(debug=True)