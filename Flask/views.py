"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import redirect
from FlaskWebProject import app

@app.route('/')
@app.route('/home')
def home():
	return render_template(
        'MainPage.html'
    )

@app.route('/nasa')
def nasaMethod():
	return redirect("http://www.seas.virginia.edu/pubs/spectra/pdfs/nasapartnerships.pdf", code=302)

@app.route('/resume')
def resumeMethod():
	return redirect("https://s3.amazonaws.com/GautamResume/GautamKanumuruResume.pdf", code=302)

@app.route('/uvradiationabstract')
def uvabstract():
	return redirect("https://s3.amazonaws.com/GautamResume/UVAbstract.pdf")

@app.route('/uvradiationpaper')
def uvpaper():
	return redirect("https://s3.amazonaws.com/GautamResume/UVPaper.pdf")

@app.route('/fieabstract')
def fieabstract():
	return redirect("https://s3.amazonaws.com/GautamResume/FIEAbstract.pdf")

@app.route('/fiepaper')
def fiepaper():
	return redirect("https://s3.amazonaws.com/GautamResume/FIEPaper.pdf")
	
@app.route('/testing')
def testMethod():
	return "Is this working"

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 Page."""
    return render_template('ErrorPage.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    """Custom 500 Page."""
    return render_template('500Error.html'), 500
