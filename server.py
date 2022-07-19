from operator import methodcaller
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
            id = session.login(user, password, ip)
            if id:
                error = 'Sucesso'
                return redirect('/mapa/')
            else:
                error = 'Usuário ou senha inválidos'
                return render_template('home.html', error=error)
    else:
        if session.getConnection(ip):
            # redirecionar para pagina do perfil?
            return redirect('/mapa/')

    return render_template('home.html')


# url to see current session connections
@app.route('/session/', methods=['GET'])
def session_url():
    text = '<h2>Connections</h2>'
    for connection in session.connections:
        text += f'<h3>connection n {session.connections.index(connection)+1}</h3>'
        text += f'<p>ip: {connection.ip}</p>'
        text += f'<p>id: {connection.id}</p>'
        text += f'<p>name: {connection.name}</p>'
        text += f'<p>member: {connection.member}</p>'
        text += f'<p>expira: {connection.expira}</p>'
    print(text)
    return text


@app.route('/mapa/', methods=['GET', 'POST'])
def map():
    ip = str(request.remote_addr)
    if not session.getConnection(ip):
        return redirect('/home/')
    else:
        if request.method == 'POST':
            if 'name-search' in request.form:
                text = request.form['name']
                # return render_template('map.html', name_feedback=text)

            elif 'cep-search' in request.form:
                text = request.form['cep']
                # return render_template('map.html', cep_feedback=text)

        return render_template('map.html')


@app.route('/logout/', methods=['GET'])
def logout():
    ip = str(request.remote_addr)
    try:
        connection = session.getConnection(ip)
        session.connections.remove(connection)
    except:
        pass

    return redirect('/home/')


@app.route('/membros/', methods=['GET', 'POST'])
def members():
    session.getMembers()
    if request.method == 'GET':
        text = ''
        for member in session.member_list:
            text += f'<h3>Membro {session.member_list.index(member)+1}</h3>'
            text += f"<p>ID: {member['id']}</p>"
            text += f"<p>Nome: {member['name']}</p>"
            text += f"<p>UF: {member['uf']}</p>"
            text += f"<p>Usuário: {member['user']}</p>"
            text += f"<p>Membro: {member['member']}</p>"

        return text
    else:
        print(request.form)
        if request.form['search'] == 'name':
            result = 'None'
            for member in session.member_list:
                if request.form['name'].lower() == member['name'].lower():
                    result = member

        return result


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5001")
