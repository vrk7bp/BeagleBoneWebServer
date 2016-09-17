from flask import Flask
from datetime import datetime
from flask import render_template
from flask import redirect
application = Flask(__name__)

@application.route('/')
@application.route('/home')
def home():
	return render_template(
        'MainPage.html'
    )

@application.route('/nasa')
def nasaMethod():
	return redirect("http://www.seas.virginia.edu/pubs/spectra/pdfs/nasapartnerships.pdf", code=302)

@application.route('/resume')
def resumeMethod():
	return redirect("https://s3.amazonaws.com/GautamResume/GautamKanumuruResume.pdf", code=302)

@application.route('/uvradiationabstract')
def uvabstract():
	return redirect("https://s3.amazonaws.com/GautamResume/UVAbstract.pdf")

@application.route('/uvradiationpaper')
def uvpaper():
	return redirect("https://s3.amazonaws.com/GautamResume/UVPaper.pdf")

@application.route('/fieabstract')
def fieabstract():
	return redirect("https://s3.amazonaws.com/GautamResume/FIEAbstract.pdf")

@application.route('/fiepaper')
def fiepaper():
	return redirect("https://s3.amazonaws.com/GautamResume/FIEPaper.pdf")
	
@application.route('/testing')
def testMethod():
	return "Is this working"

@application.errorhandler(404)
def page_not_found(e):
    """Custom 404 Page."""
    return render_template('ErrorPage.html'), 404

@application.errorhandler(500)
def page_not_found(e):
    """Custom 500 Page."""
    return render_template('500Error.html'), 500

if __name__ == "__main__":
    application.run(host='0.0.0.0')
