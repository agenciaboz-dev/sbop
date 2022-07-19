from datetime import datetime, timedelta
from src.config import TIMELIMIT, database_auth
from src.mysql_handler import Mysql


class Connection():
    def __init__(self, ip, data):
        self.ip = ip
        self.id = data[0]
        self.user = data[1]
        self.password = data[2]
        self.name = data[3]
        self.address = data[4]
        self.member = data[5]

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
        self.member_list = self.database.fetchTable(0, 'Membros')
        print(self.member_list)

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
