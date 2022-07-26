from flask import Flask, request, url_for, redirect, render_template, request
from src.session_handler import Session, Connection
from src.mysql_handler import Mysql
import src.config as cfg
import os

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
                return redirect('/perfil/')
            else:
                error = 'Usuário ou senha inválidos'
                return render_template('home.html', error=error)
    else:
        if session.getConnection(ip):
            # redirecionar para pagina do perfil?
            return redirect('/perfil/')

    return render_template('home.html')


@app.route('/perfil/', methods=['GET', 'POST'])
def member_page():
    # reconnect to database if it timed out
    if not session.database.connection.is_connected():
        session.reconnectDatabase()

    ip = str(request.remote_addr)

    if request.method == 'GET':
        connection = session.getConnection(ip)
        if not connection:
            return redirect('/home/')
    return render_template('profile.html')


@app.route('/template_restrito/', methods=['GET', 'POST'])
def template_restrito():
    ip = str(request.remote_addr)

    if request.method == 'GET':
        connection = session.getConnection(ip)
        if not connection:
            return redirect('/home/')

    return render_template('template_restrito.html')


@app.route('/cadastrar/', methods=['GET', 'POST'])
def cadastro():
    if not session.database.connection.is_connected():
        session.reconnectDatabase()
    ip = str(request.remote_addr)

    if request.method == 'GET':
        if session.getConnection(ip):
            return redirect('/home/')

        return render_template('signup.html')

    else:

        try:
            pessoa = request.form['pessoa']
        except:
            pessoa = 'None'

        cep = request.form['cep'].replace('-', '')
        # removing hyphen from text
        # cep = cep[:5] + cep[-3:]

        data = {
            'nome': request.form['nome'],
            'email': request.form['email'],
            'usuario': request.form['usuario'],
            'senha': request.form['senha'],
            'telefone': request.form['telefone'],
            'celular': request.form['celular'],
            'pessoa': pessoa,
            'endereco': request.form['endereco'],
            'numero': request.form['numero'],
            'complemento': request.form['complemento'],
            'bairro': request.form['bairro'],
            'cidade': request.form['cidade'],
            'uf': request.form['estado'],
            'pais': request.form['pais'],
            'cep': cep,
            'crm': request.form['crm'],
            'curriculum': request.form['curriculum'],
            'membro': request.form['membro']
        }
        feedback, signedup = session.signup(data)
        if not signedup:
            return render_template('signup.html', feedback=feedback)
        else:
            return f'<h1>{feedback}</h1><button onclick="window.location.href='+"'"+'/home/'+"'"+'">Voltar</button>'


@app.route('/blog_post/', methods=['GET', 'POST'])
def blog_post():

    if request.method == 'POST':
        data = {
            'member': request.form['member-type'],
            'title': request.form['title'],
            'content': request.form['content']
        }
        print(data)
        session.blogPost(data)

    return render_template('blog_post.html')


@app.route('/blog/', methods=['GET', 'POST'])
def blog():

    ip = str(request.remote_addr)

    if request.method == 'GET':
        if not session.getConnection(ip):
            return redirect('/home/')

        return render_template('blog.html')

    else:
        connection = session.getConnection(ip)
        if not connection:
            return 'False'
        else:
            return connection.member


@app.route('/get_blog/', methods=['GET'])
def get_blog():
    ip = str(request.remote_addr)
    connection = session.getConnection(ip)
    if not connection:
        return 'False'
    else:
        blog_list = session.get_blog(connection.member)
        if blog_list:
            return str(blog_list)


@app.route('/get_videos/', methods=['GET'])
def get_videos():
    ip = str(request.remote_addr)
    connection = session.getConnection(ip)
    if not connection:
        return 'False'
    else:
        # titular-1.mp4
        videos_list = os.listdir(f'static/videos/{connection.member}')

        print(videos_list)
        return str(videos_list)

# url to see current session connections


@app.route('/session/', methods=['GET'])
def session_url():
    text = '<h2>Connections</h2>'
    for connection in session.connections:
        text += f'<h3>connection n {session.connections.index(connection)+1}</h3>'
        text += f'<p>ip: {connection.ip}</p>'
        text += f'<p>id: {connection.id}</p>'
        text += f'<p>name: {connection.name}</p>'
        text += f'<p>uf: {connection.uf}</p>'
        text += f'<p>cep: {connection.cep}</p>'
        text += f'<p>member: {connection.member}</p>'
        text += f'<p>expira: {connection.expira}</p>'
    print(text)
    return text


@app.route('/mapa/', methods=['GET', 'POST'])
def map():

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


@app.route('/get_member/', methods=['GET'])
def get_member():
    ip = str(request.remote_addr)

    connection = session.getConnection(ip)
    if not connection:
        return 'False'

    data = {
        'id': connection.id,
        'name': connection.name,
        'uf': connection.uf,
        'cep': connection.cep,
        'member': connection.member
    }

    return data


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
            text += f"<p>CEP: {member['cep']}</p>"
            text += f"<p>Usuário: {member['user']}</p>"
            text += f"<p>Membro: {member['member']}</p>"

        return text
    else:
        result = []

        # name search request
        if request.form['search'] == 'name':
            searched = request.form['name'].lower()
            for member in session.member_list:
                if searched in member['name'].lower():
                    result.append(member)

        # cep search request
        elif request.form['search'] == 'cep':
            for member in session.member_list:
                if request.form['cep'].lower() == member['cep'].lower():
                    result.append(member)

        elif request.form['search'] == 'uf':
            for member in session.member_list:
                if request.form['uf'] == member['uf'].lower():
                    result.append(member)

        return str(result)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5001")
