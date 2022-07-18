from flask import Flask, request, url_for, redirect, render_template, request
from src.session_handler import Session, Connection

session = Session()
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    # redirecting to another endpoint
    return redirect(url_for('home'))


@app.route('/home/', methods=['GET', 'POST'])
def home():

    ip = str(request.remote_addr)
    if request.method == 'POST':
        global session
        if 'login' in request.form:
            user = request.form['user']
            password = request.form['password']

    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")
