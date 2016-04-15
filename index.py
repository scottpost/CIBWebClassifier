import csv
from nltk import tokenize
from classifier import ArticleClassificationPackage
from flask import Flask, flash, url_for, session, request, redirect, render_template

# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

SENTENCES = ""
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form['username']
		session['password'] = request.form['password']
		try:
		    database = ArticleClassificationPackage(username, password)
		    flash('You were successfully logged in')
		    return redirect(url_for('classify'))
		except:
		    flash('Incorrect authentication details', 'error')
		    return render_template('show_entries.html', logged = False, sentences = [])
	return render_template('show_entries.html', logged = False, sentences = [])

@app.route('/classify', methods=['GET', 'POST'])
def classify():

	if request.method == 'POST' and request.form['button'] == 'generate':
		sentences = []
		try:
			username = session.get('username', None)
			password = session.get('password', None)
			database = ArticleClassificationPackage(username, password)
			text = database.get_article()['text']
			if text != None:
				sentences = tokenize.sent_tokenize(text)
				for sentence in sentences:
					if len(sentence) < 40:
						sentences.remove(sentence)
		except:
			sentences = []
		return render_template('show_entries.html', logged = True, sentences = sentences)

	if request.method == 'POST' and request.form['button'] == 'generateArticle':
		sentences = []
		try:
			username = session.get('username', None)
			password = session.get('password', None)
			database = ArticleClassificationPackage(username, password)
			text = database.get_article()['text']
			sentences = [text]
		except:
			sentences = []
		return render_template('show_entries.html', logged = True, sentences = sentences)


	if request.method == 'POST' and request.form['button'] == 'submit':
		positives = request.form.getlist("Positive")
		negatives = request.form.getlist("Negative")
		strongs = request.form.getlist("Strong")
		weaks = request.form.getlist("Weak")

		sentenceDict = {}
		for sentence in positives:
			sentenceDict[sentence] = [1, 0, 0, 0]

		for sentence in negatives:
		    sentenceDict[sentence] = [0, 1, 0, 0]
		for sentence in strongs:
		    if sentence in sentenceDict.keys():
		        sentenceDict[sentence][2] = 1
		        sentenceDict[sentence][3] = 0
		    else:
		        sentenceDict[sentence] = [0, 0, 1, 0]
		for sentence in weaks:
		    if sentence in sentenceDict.keys():
		        sentenceDict[sentence][2] = 0
		        sentenceDict[sentence][3] = 1
		    else:
		        sentenceDict[sentence] = [0, 0, 0, 1]

		with open("/home/spost/CIB/output.csv", "a") as fp:
			wr = csv.writer(fp, dialect='excel')
			print "Writing to file"
			for key in sentenceDict:
				row = [key.encode("utf-8"), sentenceDict[key][0], sentenceDict[key][1], sentenceDict[key][2], sentenceDict[key][2]]
				wr.writerow(row)

		return render_template('show_entries.html', logged = True, sentences=[])
	return render_template('show_entries.html', logged = True, sentences=[])

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()