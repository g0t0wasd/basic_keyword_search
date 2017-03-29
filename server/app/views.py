from app import app
from flask import render_template

# Views
@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Dima'}
    return render_template('index.html', title="Home",
                           user=user)