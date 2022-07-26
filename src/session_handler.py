from datetime import datetime, timedelta, date
from src.config import TIMELIMIT, database_auth
from src.mysql_handler import Mysql


class Connection():
    def __init__(self, ip, data):
        self.ip = ip
        self.id = data[0]
        self.user = data[1]
        self.password = data[2]
        self.name = data[3]
        self.uf = data[4]
        self.member = data[5]
        self.cep = data[6]

        self.expira = datetime.now() + timedelta(minutes=TIMELIMIT)

    def isExpired(self):
        if not datetime.now() < self.expira:
            return True


class Session():
    def __init__(self):
        self.connections = []
        self.member_list = []
        self.database = Mysql()
        self.database.connect(database_auth)
        self.getMembers()

    def getMembers(self):
        if not self.database.connection.is_connected():
            self.reconnectDatabase()

        self.member_list = []
        members = self.database.fetchTable(0, 'Membros')

        for member in members:
            data = {
                'id': member[0],
                'user': member[1],
                'name': member[3],
                'uf': member[4],
                'member': member[5],
                'cep': member[6]
            }
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
        try:
            data = self.database.fetchTable(1, 'Membros', 'USUÁRIO', user)[0]
            if data:
                if password == data[2]:
                    id = data[0]

                    # check if user is already logged and update it' connection if it exists
                    is_logged = self.getConnection(ip)
                    if is_logged and is_logged.id == id:
                        self.connections.remove(is_logged)

                    self.connections.append(Connection(ip, data))
                    return str(id)
        except Exception as error:
            print(error)
            return None

    def signup(self, data):
        try:
            usuario = self.database.fetchTable(
                1, 'Membros', 'USUÁRIO', data['usuario'])[0]
            if usuario:
                return 'Usuário já cadastrado', False

            email = self.database.fetchTable(
                1, 'Membros', 'EMAIL', data['email'])[0]
            if email:
                return 'E-mail já cadastrado', False

        except:
            data.update({'id': len(self.member_list)})
            self.database.insertMember(data)
            return 'Usuário cadastrado', True

    def get_blog(self, membro):
        try:
            blog_list = self.database.fetchTable(0, 'Blog', 'MEMBRO', membro)
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
