from flask import Flask, request, url_for, redirect, render_template, request
from src.session_handler import Session, Connection
from src.mysql_handler import Mysql
import src.config as cfg


session = Session()
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    # redirecting to another endpoint
    return redirect(url_for('home'))


@app.route('/home/', methods=['GET', 'POST'])
def home():
    # reconnect to database if it timed out
    if not session.database.connection.is_connected():
        session.reconnectDatabase()

    ip = str(request.remote_addr)
    if request.method == 'POST':
        if 'login' in request.form:
            user = request.form['user']
            password = request.form['password']
            id = session.login(user, password)
            if id:
                error = 'Sucesso'
                return render_template('home.html', error=error)
            else:
                error = 'Usuário ou senha inválidos'
                return render_template('home.html', error=error)

    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")
