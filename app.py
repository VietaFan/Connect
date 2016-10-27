#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
#from flask_heroku import Heroku #online hosting package
import logging
from logging import Formatter, FileHandler
import os
import userMatcher
#from flask.ext.googlemaps import GoogleMaps
#from flask.ext.googlemaps import Map
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
#heroku = Heroku(app)
app.config.from_object('config')
#GoogleMaps(app)
#<<<<<<< HEAD
#=======
#from models import User # needs to be after app is declared
#>>>>>>> af1add2edbfeab75cc5ec0756fb8e49fab9513ac

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
#need jsonify imported for ajax to work
# Ajax call handler - Server side
fieldNames = ['Timestamp', 'Name', 'ID', 'Phone number', 'Email', 'Gender', 'How friendly were the staff?', 'How efficient was the process?', 'Overall Satisfaction?', 'Ethnicity', 'Age', 'Are you a veteran?', 'Have you been diagnosed with any of the following?', 'What is your current monthly income?', 'Where were you living prior to coming here?', 'Why did you choose to come here? [Rent/Utility bills]', 'Why did you choose to come here? [Prescription/Medical bills]', 'Why did you choose to come here? [Loss of wages]', 'Why did you choose to come here? [Family expenses]', 'Why did you choose to come here? [Death in family]', 'Why did you choose to come here? [Relocation costs]', 'Why did you choose to come here? [Domestic violence]', 'Why did you choose to come here? [Needed food]', 'Why did you choose to come here? [Needed clothing]', 'Why did you choose to come here? [Wanted information about shelters]', 'How did you hear of this program?', '"If you were referred to this program by another participant please enter your referrer\'s name below."', 'Which problems were you looking to solve? [Receiving money]', 'Was it made clear how the program worked?', 'Overall Impression of Staff?', 'Any other information we should know about you?', 'Which problems were you looking to solve? [Receiving vouchers for goods/items]', 'Which problems were you looking to solve? [Receiving referral information]', 'Which problems were you looking to solve? [Receiving housing]', 'Which problems were you looking to solve? [Receiving counseling]', 'How well did the staff understand your situation?', 'Please rank the helpfulness of the following services for you to the best of your ability. [Reception/General Efficiency]', '"What was the approximate zipcode of your location prior to arriving here?  If you are not sure or do not wish to answer please write N/A."', 'Please rank the helpfulness of the following services for you to the best of your ability. [Meal Provisions]', 'Please rank the helpfulness of the following services for you to the best of your ability. [Health and Disabilities Services]', 'Please rank the helpfulness of the following services for you to the best of your ability. [Substance Abuse Services]', 'Please rank the helpfulness of the following services for you to the best of your ability. [Domestic Violence Services]', 'Please rank the helpfulness of the following services for you to the best of your ability. [Employment and Education Services]', 'Please rank the helpfulness of the following services for you to the best of your ability. [Energy and Housing Assistance]', 'Please rank the helpfulness of the following services for you to the best of your ability. [Receiving Money and Goods]', 'Please rank the helpfulness of the following services for you to the best of your ability. [Legal Services]', 'Please rank the following services of this program to the best of your ability. [Housing Services]', 'Please rank the following services of this program to the best of your ability. [Technology Services]', 'Please rank the following services of this program to the best of your ability. [Religious Resources]', 'Please rank the following services of this program to the best of your ability. [Comm]', 'Please rank the helpfulness of the following services for you to the best of your ability. [Hygiene Care]', 'Please rank the helpfulness of the following services for you to the best of your ability. [Technology Services]', 'Please rank the helpfulness of the following services for you to the best of your ability. [Finding Communities]', 'Please rank the helpfulness of the following services for you to the best of your ability. [Receiving Information and Resources]', 'Please rank the helpfulness of the following services for you to the best of your ability. [Counseling Services]', 'Please rank the helpfulness of the following services for you to the best of your ability. [Housing Services]', 'Please rank the helpfulness of the following services for you to the best of your ability. [Finding Religious Communities]', 'Any additional comments?', 'Were there any services which you would like to see improved?', 'Were there any services which particularly impressed you?', 'Any other information?', 'Wa', 'Why did you choose to come here? [Row 11]', 'Why did you choose to come here? [Row 4]']

@app.route('/ajaxtest', methods=['POST'])
def testAjax():
    n = int(request.form['exponent'])
    return jsonify({'power2': str(2**n),
                    'power3': str(3**n)})

@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

# People pages
@app.route('/seeking', methods=['GET', 'POST'])
def seeking():
    if request.method == 'POST':
        print(request.form)
        return render_template('pages/seeking.html')
    return render_template('pages/seeking.html')

@app.route('/orgs')
def organizations():
    return render_template('pages/organizations.html')

@app.route('/vols')
def volunteers():
    return render_template('pages/volunteers.html')

@app.route('/matcher', methods=['GET', 'POST'])
def connectMatcher():
    if request.method == 'POST':
        x = userMatcher.getUser(request.form['field'])
        if x == None:
            return render_template('pages/connect_matcher.html', error=True)
        L = userMatcher.getSimilarList(x)
        matches = []
        for i in range(min(len(L),5)):
            if not L[i][0]: break
            matches.append({'rank':i+1,
                            'name':L[i][1][1],
                            'email':L[i][1][3],
                            'sim':L[i][0]})
        return render_template('pages/connect_matcher.html', matches=matches)
    return render_template('pages/connect_matcher.html')

# Connect pages
@app.route('/connect-seek')
def connect_seek():
    return render_template('pages/connect_seek.html')

@app.route('/connect-orgs')
def connect_orgs():
    return render_template('pages/connect_orgs.html')

@app.route('/connect-vols')
def connect_vols():
    return render_template('pages/connect_vols.html')

# Error handlers.
@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
