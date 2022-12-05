from datetime import datetime, timedelta, date
from src.config import TIMELIMIT, database_auth, google_api_key
from src.mysql_handler import Mysql
from src.mail_sender import sendMail
from cryptography.fernet import Fernet
import json
import requests
import geopy.distance
from src.mail_templates import recoverPasswordTemplate


class Connection():
    def __init__(self, ip, database, id):
        self.id = id
        self.buildAttributes(ip, database)

        self.expira = datetime.now() + timedelta(minutes=TIMELIMIT)

    def isExpired(self):
        if not datetime.now() < self.expira:
            return True

    def buildAttributes(self, ip, database):
        data = database.fetchTable(1, 'Membros', 'id', self.id)[0]
        self.ip = ip
        self.user = data[1]
        self.password = data[2]
        self.name = data[3]
        self.uf = data[4]
        self.member = data[5]
        self.cep = data[6]
        self.email = data[7]
        self.telefone = data[8]
        self.celular = data[9]
        self.endereco = data[10]
        self.numero = data[11]
        self.complemento = data[12]
        self.bairro = data[13]
        self.cidade = data[14]
        self.pais = data[15]
        self.crm = data[16]
        self.curriculum = data[17]
        self.pessoa = data[18]
        self.temporario = data[19]
        self.primeiro_acesso = data[20]
        self.cpf = data[21]
        self.especialidades = []
        self.pago = data[23]
        self.adm = data[24]
        for item in data[22].split(','):
            self.especialidades.append(item)
        self.solicitacoes = database.fetchTable(
            0, 'Solicitacoes', 'USUARIO', self.id, ordered='id')
        self.solicitacoes.reverse()


class Session():
    def __init__(self):
        self.connections = []
        self.member_list = []
        self.solicitacoes_disponiveis = []
        self.database = Mysql()
        self.database.connect(database_auth)
        self.getMembers()
        self.getSolicitacoes()

    def getSolicitacoes(self):
        self.solicitacoes_disponiveis = self.database.fetchTable(
            0, 'available_requests')

    def buildMember(self, member):
        data = {
            'id': member[0],
            'user': member[1],
            'password': member[2],
            'name': member[3],
            'uf': member[4],
            'member': member[5],
            'cep': member[6],
            'email': member[7],
            'telefone': member[8],
            'celular': member[9],
            'endereco': member[10],
            'numero': member[11],
            'complemento': member[12],
            'bairro': member[13],
            'cidade': member[14],
            'pais': member[15],
            'crm': member[16],
            'curriculum': member[17],
            'pessoa': member[18],
            'temporario': member[19],
            'primeiro_acesso': member[20],
            'cpf': member[21],
            'especialidades': member[22],
            'pago': member[23],
            'adm': member[24],
            'lat': member[25],
            'lng': member[26],
        }
        return data

    def getMembers(self):
        try:
            if not self.database.connection.is_connected():
                self.reconnectDatabase()
        except:
            pass

        self.member_list = []
        sql = 'SELECT * FROM Membros ORDER BY nome ASC'
        members = self.database.run(sql)

        for member in members:
            data = self.buildMember(member)
            self.member_list.append(data)

    def reconnectDatabase(self):
        self.database.connect(database_auth)

    def getConnection(self, ip):
        for connection in self.connections:
            if connection.ip == ip:
                if not connection.isExpired():
                    return connection
                else:
                    self.connections.remove(connection)

    def login(self, user, password, ip):
        cpf = None
        email = None
        try:
            cpf = int(user)
        except:
            pass

        if '@' in user:
            email = True

        if cpf:
            column = 'cpf'
        elif email:
            column = 'email'
        else:
            column = 'user'

        try:
            sql = f"SELECT * FROM Membros WHERE {column} = '{user}' ;"
            data = self.database.run(sql)[0]
            print(data)
            # data = self.database.fetchTable(1, 'Membros', column, user)[0]
            if data:
                if password == data[2]:
                    id = data[0]

                    # check if user is already logged and update it' connection if it exists
                    is_logged = self.getConnection(ip)
                    if is_logged and is_logged.id == id:
                        self.connections.remove(is_logged)

                    connection = Connection(ip, self.database, id)
                    self.connections.append(connection)
                    return [str(id), connection]
        except Exception as error:
            print(error)
            return None

    def signup(self, data):
        try:
            usuario = self.database.fetchTable(
                1, 'Membros', 'user', data['user'])
            if usuario:
                return {'error': 'Usuário já cadastrado'}

            email = self.database.fetchTable(
                1, 'Membros', 'email', data['email'])
            if email:
                return {'error': 'E-mail já cadastrado'}
            
            cpf = self.database.fetchTable(
                1, 'Membros', 'cpf', data['cpf'])
            if cpf:
                return {'error': 'CPF já cadastrado'}
            
            raise ValueError('erro')

        except:
            coords = self.getCoords(data['cep'])
            data.update({'lat': coords[0], 'lng': coords[1]})
            self.database.insertMember(data)
            self.member_list.append(data)
            return {'success': 'Usuário cadastrado'}

    def get_blog(self, membro):
        try:
            blog_list = self.database.fetchTable(
                0, 'Blog', 'assinatura', membro)
            if blog_list:
                return blog_list
        except:
            return None

    def blogPost(self, data):
        id = len(self.database.fetchTable(0, 'Blog'))
        date = datetime.now()
        date = f'{date.day}/{date.month}/{date.year} - {date.hour}:{date.minute}'
        data = (id, data['member'], data['title'],
                data['content'], data['author'], date)
        self.database.insertPost(data)

    def editMember(self, data):
        try:
            if not self.database.connection.is_connected():
                self.reconnectDatabase()
        except:
            pass
        if data.get('adm_panel'):
            telefone = 'telefone'
            especialidades = 'especialidades'
            user='user'
            
            member = self.database.run(f"SELECT * FROM Membros WHERE id={data['id']}", json=True)[0]
            if not member['user'] == data['user']:
                new_user = self.database.run(f"SELECT * FROM Membros WHERE user = '{data['user']}'")
                if new_user:
                    return {'error': 'Nome de usuário já cadastrado'}
        else:
            telefone = 'telefone_plain'
            especialidades = 'especialidades_str'
            user = 'username'

        try:
            sql = f"""UPDATE Membros SET 
                user='{data[user]}', 
                senha='{data['password']}', 
                nome='{data['name']}', 
                uf='{data['uf']}', 
                cep='{data['cep']}', 
                cpf='{data['cpf']}', 
                email='{data['email']}', 
                crm='{data['crm']}', 
                curriculum='{data['curriculum']}', 
                telefone='{data[telefone]}', 
                endereco='{data['endereco']}', 
                numero='{data['numero']}', 
                complemento='{data['complemento']}', 
                bairro='{data['bairro']}', 
                cidade='{data['cidade']}', 
                especialidades='{data[especialidades]}', 
                temporario='{data['temporario']}', 
                pago='{data['pago']}', 
                primeiro_acesso='{data['primeiro_acesso']}' 
                WHERE id={data['id']}"""
                
            print(sql)
            cursor = self.database.connection.cursor()
            cursor.execute(sql)
            self.database.connection.commit()
            cursor.close()
            return 'True'
        except Exception as error:
            print(error)
            return 'False'

    def getEspecialidades(self):
        try:
            if not self.database.connection.is_connected():
                self.reconnectDatabase()
        except:
            pass
        sql = 'SELECT nome FROM especialidades order by id;'
        print(sql)
        data = self.database.run(sql, json=True)
        print(data)

        return data

    def setEspecialidades(self, data):
        try:
            if not self.database.connection.is_connected():
                self.reconnectDatabase()
        except:
            pass
        sql = f"UPDATE Membros SET ESPECIALIDADES='{data['especialidades']}' WHERE ID={data['id']}"
        print(sql)
        try:
            self.database.run(sql)
        except Exception as error:
            print(error)
        finally:
            return {'especialidades': data['especialidades']}

    def getCepDistance(self, origem, destino):
        distance = geopy.distance.geodesic(origem, destino).km

        return distance

    def getCoords(self, address):
        address = address.replace(' ', '+')
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_api_key}'
        print(url)
        response = json.loads(requests.get(url).text)
        if response['results']:
            location = response['results'][0]['geometry']['location']

            return (location['lat'], location['lng'])

    def trySendMail(self, encrypted, username):
        sql = f"SELECT * FROM Membros WHERE user='{username}' ;"
        result = self.database.run(sql, json=True)

        if result:
            link = f"""http://sistema.sbop.com.br:5001/recover?user={encrypted}"""
            message = recoverPasswordTemplate(username, link)
            sendMail(result[0]['email'],
                     "Sbop - Recuperar senha", html=message)
            return {'msg': f'Um link para redefinição de senha foi enviado para o e-mail do usuário'}
        else:
            return {'msg': 'Usuário não encontrado'}

    def encrypt(self, text):
        key = b'XJix9-kcLVndopzt3V61Mogzwn_e5xag1vsGlTIFeP4='
        cipher = Fernet(key)
        encrypted = cipher.encrypt(text.encode())

        return encrypted

    def decrypt(self, encrypted):
        key = b'XJix9-kcLVndopzt3V61Mogzwn_e5xag1vsGlTIFeP4='
        cipher = Fernet(key)
        decrypted = cipher.decrypt(encrypted).decode()

        return decrypted

    def getUser(self, username):
        sql = f"SELECT * FROM Membros WHERE user = '{username}' ;"
        result = self.database.run(sql, json=True)
        print(result)

        return result[0] if result else None

    def changePassword(self, data):
        sql = f"UPDATE Membros SET senha = '{data['senha']}' WHERE id = {data['id']} ;"
        try:
            self.database.run(sql, commit=True)
            return {'success': 'senha alterada'}
        except Exception as error:
            print(error)
            return {'error': 'error'}

    def getPosts(self, data):
        try:
            if not self.database.connection.is_connected():
                self.reconnectDatabase()
        except:
            pass
        sql = f"SELECT * FROM conteudos WHERE titulo like '%{data['searched']}%' order by id desc;"
        data = self.database.run(sql, json=True)
        print(data)

        return data

    def getPost(self, data):
        sql = f"SELECT * FROM conteudos WHERE id = {data['id']} ;"
        post = self.database.run(sql, json=True)

        return post

    def editPost(self, data):
        sql = f"""UPDATE conteudos SET 
                titulo = '{data['titulo']}',
                assinatura = '{data['assinatura']}',
                categoria = '{data['categoria']}',
                conteudo = '{data['conteudo']}',
                resumo = '{data['resumo']}'
                
                WHERE id = {data['id']} ;
        """
        try:
            self.database.run(sql, commit=True)
            return {'success': 'postagem alterada com sucesso'}
        except Exception as error:
            print(error)
            return {'error': error}

    def newPost(self, data):

        sql = f"""INSERT INTO conteudos 
            (video, assinatura, categoria, resumo, titulo, conteudo, autor, data)
            VALUES
            ({data['video']}, '{data['assinatura']}', '{data['categoria']}' ,'{data['resumo']}', '{data['titulo']}', '{data['conteudo']}', '{data['autor']}', '{data['data']}' )
        """
        try:
            self.database.run(sql, commit=True)
            id = self.database.run(
                'select * from conteudos order by id desc limit 1', json=True)[-1]['id']
            return {'success': 'publicacao inserida', 'id': id}
        except Exception as error:
            print(error)
            return {'error': error}
        
    def deletePost(self, id):
        sql = f"""DELETE FROM conteudos WHERE id = {id} ;"""
        try:
            self.database.run(sql, commit=True)
            return {'success': f'${id} deleted'}
        except Exception as error:
            print(error)
            return {'error': error}

    def getMemberPosts(self, assinatura):
        posts = []
        sql = f"SELECT * FROM conteudos ORDER BY id DESC ;"
        data = self.database.run(sql, json=True)
        for post in data:
            if post['assinatura'] == 'Aspirante':
                posts.append(post)

            if post['assinatura'] == 'Associado':
                if assinatura == 'Associado' or assinatura == 'Titular':
                    posts.append(post)

            if post['assinatura'] == 'Titular':
                if assinatura == 'Titular':
                    posts.append(post)

        return posts

    def sendDocuments(self, data, attachment):
        sendMail('noreply@sbop.com.br',
                 f'Sbop - Documentação titularidade - {data["membro"]["nome"]}', json.dumps(data), attachment)
        return {'teste': 'teste'}
