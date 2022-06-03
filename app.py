from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/movie-details')
def movieDetails():
    return render_template('movie-details.html')

@app.route('/landing')
def landing():
    return render_template('landing-page.html')