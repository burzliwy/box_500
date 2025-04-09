from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/organizer/dashboard')
def organizer_dashboard():
    return render_template('organizer_dashboard.html')

@app.route('/game')
def game():
    return render_template('game.html')

if __name__ == '__main__':
    app.run(debug=True)


