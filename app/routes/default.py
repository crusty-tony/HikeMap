from app import app
from flask import render_template

# This is for rendering the home page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/description')
def description():
    return render_template('description.html')

@app.route('/pretendprofile')
def pretendprofile():
    return render_template('pretendprofile.html')