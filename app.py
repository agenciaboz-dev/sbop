from datetime import datetime
from flask import Flask, request, url_for, redirect, render_template, request
from flask_cors import CORS
from src.session_handler import Session
from src.mysql_handler import Mysql
import src.config as cfg
import os
import json

session = Session()
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    # redirecting to another endpoint
    return redirect(url_for('home'))


@app.route('/home/', methods=['GET', 'POST'])
def home():
    # reconnect to database if it timed out
    try:
        if not session.database.connection.is_connected():
            session.reconnectDatabase()
    except:
        pass

    ip = str(request.remote_addr)
    if request.method == 'POST':
        if 'login' in request.form:
            user = request.form['user']
            password = request.form['password']
            connection = session.login(user, password, ip)
            if connection:
                if connection[0]:
                    print(connection[1].adm)
                    if connection[1].adm:
                        return redirect('/adm/')
                    return redirect('/perfil/')
            else:
                error = 'Usuário ou senha inválidos'
                return render_template('home.html', error=error)
    else:
        if session.getConnection(ip):
            # redirecionar para pagina do perfil?
            return redirect('/perfil/')

    return render_template('home.html')


@app.route('/adm/', methods=['GET'])
def adm_page():
    ip = str(request.remote_addr)
    connection = session.getConnection(ip)
    if not connection:
        return redirect('/home/')
    else:
        if not connection.adm:
            return redirect('/perfil/')
    
    return render_template('adm.html')


@app.route('/adm_posts/', methods=['GET'])
def adm_posts_page():
    ip = str(request.remote_addr)
    connection = session.getConnection(ip)
    try:
        if not session.database.connection.is_connected():
            session.reconnectDatabase()
    except:
        pass
    
    if not connection:
        return redirect('/home/')
    else:
        if not connection.adm:
            return redirect('/perfil/')

    return render_template('adm_posts.html')

@app.route('/adm_new_post/', methods=['GET'])
def adm_new_post_page():
    ip = str(request.remote_addr)
    connection = session.getConnection(ip)
    try:
        if not session.database.connection.is_connected():
            session.reconnectDatabase()
    except:
        pass
    
    if not connection:
        return redirect('/home/')
    else:
        if not connection.adm:
            return redirect('/perfil/')

    return render_template('adm_new_post.html')


@app.route('/perfil/', methods=['GET', 'POST'])
def member_page():
    # reconnect to database if it timed out
    try:
        if not session.database.connection.is_connected():
            session.reconnectDatabase()
    except:
        pass

    ip = str(request.remote_addr)

    if request.method == 'GET':
        connection = session.getConnection(ip)
        if not connection:
            return redirect('/home/')
    return render_template('profile.html')


@app.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    try:
        if not session.database.connection.is_connected():
            session.reconnectDatabase()
    except:
        pass
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
        # feedback, signedup = session.signup(data)
        # if not signedup:
        #     return render_template('signup.html', feedback=feedback)
        # else:
            # return f'<h1>{feedback}</h1><button onclick="window.location.href='+"'"+'/home/'+"'"+'">Voltar</button>'
        return f'<h1>Em desenvolvimento</h1><button onclick="window.location.href='+"'"+'/home/'+"'"+'">Voltar</button>'


@app.route('/blog_post/', methods=['GET', 'POST'])
def blog_post():

    if request.method == 'POST':
        data = {
            'author': request.form['author'],
            'member': request.form['member-type'],
            'title': request.form['title'],
            'content': request.form['content']
        }
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

# get content


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

# get videos


@app.route('/get_videos/', methods=['GET'])
def get_videos():
    ip = str(request.remote_addr)
    connection = session.getConnection(ip)
    if not connection:
        return 'False'
    else:
        # titular-1.mp4
        videos_list = os.listdir(f'static/videos/{connection.member}')

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
    try:
        if not session.database.connection.is_connected():
            session.reconnectDatabase()
    except:
        pass

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
    connection.buildAttributes(ip, session.database)
    if not connection:
        return 'False'

    data = vars(connection)

    return data


# search members or get all members
@app.route('/membros/', methods=['GET', 'POST'])
def members():
    session.getMembers()
    if request.method == 'GET':
        data = session.member_list
        nova_data = json.dumps(data)
        return nova_data
    else:
        result = [request.form['value']]
        try:
            if request.form['adm']:
                adm = True
        except:
            adm = False

        # name search request
        if request.form['search'] == 'name':
            searched = request.form['value'].lower()
            sql = f"SELECT * FROM `Membros` WHERE nome like '%{searched}%' AND assinatura = 'Titular' ORDER BY nome ASC"
            if adm:
                sql = f"SELECT * FROM `Membros` WHERE nome like '%{searched}%' ORDER BY nome ASC"
            members = session.database.run(sql)
            for member in members:
                data = session.buildMember(member)
                result.append(data)


        # cep search request
        elif request.form['search'] == 'cep':

            distances = []
            coords = session.getCoords(request.form['value'])
            for member in session.member_list:
                if member['member'] == 'Titular':
                    member_cep_str = member['cep']
                    try:
                        member_cep = int(member_cep_str)
                        distance = session.getCepDistance(coords, (member['lat'], member['lng']))
                        this_member = {
                            'distance': distance
                        }
                        this_member.update(member)
                        distances.append(this_member)

                    except:
                        continue
                    
            sorted_distances = sorted(distances, key=lambda d: d['distance'])
            result.extend(sorted_distances[:7])
                

        # map search
        elif request.form['search'] == 'uf':
            sql = f"SELECT * FROM `Membros` WHERE uf = '{request.form['value'].upper()}' AND assinatura = 'Titular' ORDER BY nome ASC"
            members = session.database.run(sql)
            for member in members:
                data = session.buildMember(member)
                result.append(data)

        result = json.dumps(result)
        return result


# get map statuses
@app.route('/get_map_status/', methods=['GET'])
def get_map_status():
    try:
        if not session.database.connection.is_connected():
            session.reconnectDatabase()
    except:
        pass
    users = session.database.fetchTable(0, 'Membros')

    medicos = []
    estados = []
    cidades = []

    for item in users:
        if item[5] == 'Titular':
            medicos.append(users)
            if item[4] not in estados:
                estados.append(item[4])

            if item[14] not in cidades:
                cidades.append(item[14])

    data = {
        'medicos': len(medicos) // 10 * 10,
        'estados': len(estados) // 5 * 5,
        'cidades': len(cidades) // 5 * 5,
        'real_medicos': len(medicos),
        'real_estados': len(estados),
        'real_cidades': len(cidades)
    }
    return data


@app.route('/estados_data/', methods=['GET'])
def estados_data():
    estados = []
    for item in session.member_list:
        if item['member'] == 'Titular':
            estados.append(item['uf'].lower())
    return str(estados)


# get available requests
@app.route('/available_requests/', methods=['GET'])
def available_requests():
    return str(session.solicitacoes_disponiveis)


# change member type/plan
@app.route('/change_plan/', methods=['POST'])
def change_plan():
    session.database.updateTable(
        'Membros', request.form['id'], 'assinatura', request.form['plan'], 'ID')
    return 'True'


# change user password
@app.route('/change_password/', methods=['POST'])
def change_password():
    try:
        id = request.form['id']
        session.database.updateTable(
            'Membros', id, 'senha', request.form['new_password'], 'ID')
        if 'first_access' in request.form:
            session.database.updateTable(
                'Membros', id, 'primeiro_acesso', 'False', 'ID')
        return str(['Sucesso', 'Sua senha foi alterada'])
    except Exception as error:
        return str(['Erro', error])


# change user email
@app.route('/change_email/', methods=['POST'])
def change_email():
    try:
        session.database.updateTable(
            'Membros', request.form['id'], 'email', request.form['new_email'], 'id')
        return str(['Sucesso', 'Seu e-mail foi alterado'])
    except Exception as error:
        return str(['Erro', error])


# request to cancel a pending request
@app.route('/cancel_request/', methods=['POST'])
def cancel_request():
    id = request.form['id']
    try:
        session.database.updateTable(
            'Solicitacoes', id, 'SITUACAO', 'Encerrado', 'ID')
        return str(['Sucesso', 'Solicitação cancelada, me dá um email pra notificar'])
    except Exception as error:
        print(error)
        return str(['Erro', error])


# make a request
@app.route('/new_request/', methods=['POST'])
def new_request():
    solicitacao = session.database.fetchTable(
        1, 'available_requests', 'id', request.form['request'])[0][1]
    request_id = len(session.database.fetchTable(0, 'Solicitacoes'))
    time = datetime.today()
    day = time.day
    month = time.month
    year = time.year

    if len(str(day)) == 1:
        day = f'0{day}'

    if len(str(month)) == 1:
        month = f'0{month}'

    today = f'{day}/{month}/{year}'

    protocolo = f'{request.form["id"]}.{request.form["request"]}.{request_id}.{day}.{month}.{year}'

    data = (request_id,
            request.form['id'], solicitacao, 'Em Andamento', today, '', protocolo)
    try:
        # ID, USUARIO, SOLICITACAO, SITUACAO, DATA, URL
        session.database.insertRequest(data)
        new = [request_id, request.form['id'],
               solicitacao, 'Em Andamento', today, '', protocolo]
        session.getConnection(request.remote_addr).solicitacoes.insert(0, new)
        return str(['Sucesso', 'Sua solicitação foi registrada, me dá um email pra notificar', solicitacao, today, protocolo])
    except Exception as error:
        return str([error, error, error, error, error])


# update profile data
@app.route('/update_profile/', methods=['POST'])
def update_profile():
    response = session.editMember(request.form)

    return response


# remove temporary flag
@app.route('/remove_temporary/', methods=['POST'])
def remove_temporary():
    try:
        session.database.updateTable(
            'Membros', request.form['id'], 'temporario', 'False', 'ID')
        return 'True'
    except Exception as error:
        print(error)
        return 'False'
    
@app.route('/edit_member/', methods=["POST"])
def edit_member():
    data = request.get_json()
    print(data)
    response = session.editMember(data)

    return json.dumps(response)

@app.route('/get_posts/', methods=['POST'])
def get_posts():
    data = request.get_json()
    response = session.getPosts(data)

    return json.dumps(response)

@app.route('/especialidades/', methods=['GET'])
def especialidades():
    especialidades = session.getEspecialidades()

    return json.dumps(especialidades)

@app.route('/trocar_especialidade/', methods=['POST'])
def trocar_especialidade():
    data = request.get_json()

    response = session.setEspecialidades(data)
    return json.dumps(response)

@app.route('/recuperar/', methods=['POST'])
def recuperar_route():
    data = request.get_json()

    encrypted = session.encrypt(data['user'])
    response = session.trySendMail(encrypted, data['user'])
    print(response)
    return json.dumps(response)

@app.route('/recover/', methods=['GET', 'POST'])
def recover():
    if request.method == 'GET':
        data = request.args.get('user')
        
        decrypted = session.decrypt(data.encode())
        user = session.getUser(decrypted)
        print(data)
        
        return render_template('recuperar_senha.html', usuario=user['user'], id=user['id'])

    else:
        data = request.get_json()
        print(data)
        response = session.changePassword(data)
        print(response)
        return json.dumps(response)
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5001")
