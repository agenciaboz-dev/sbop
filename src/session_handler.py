from datetime import datetime, timedelta
from src.config import TIMELIMIT, database_auth
from src.mysql_handler import Mysql


class Connection():
    def __init__(self, ip, id):
        self.ip = ip
        self.id = id
        self.expira = datetime.now() + timedelta(minutes=TIMELIMIT)

    def isExpired(self):
        if not datetime.now() < self.expira:
            return True


class Session():
    def __init__(self):
        self.connections = []
        self.database = Mysql()
        self.database.connect(database_auth)

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
                    self.connections.append(Connection(ip, id))
                    return str(id)
        except Exception as error:
            print(error)
            return None
