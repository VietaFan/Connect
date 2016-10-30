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
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
#heroku = Heroku(app)
app.config.from_object('config')
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

@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')

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
