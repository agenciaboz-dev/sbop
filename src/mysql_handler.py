import mysql.connector
import src.config


class Mysql():
    # def __init__(self) -> None:
    #     pass

    def connect(self, auth):
        ''' Try to connect to a database with auth params defined in config file '''
        try:
            self.connection = mysql.connector.connect(host=auth['host'],
                                                      database=auth['database'],
                                                      user=auth['user'],
                                                      password=auth['password'])
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self.connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                # cursor.close()
                self.auth = auth

                return self.connection

        except Exception as e:
            print(e)

    def disconnect(self):
        ''' Disconnect from database '''
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

    def fetchTable(self, rows, table, condition=None, value=None, reversed=None):
        ''' Fetch a number of rows from a table that exists in database.
        Number of rows and table defined in config file.
        if number of rows equals to 0, will try to fetch all rows.'''

        if condition:
            sql = f'SELECT * FROM `{table}` WHERE {condition} = "{value}"'
            if reversed:
                sql = f'SELECT * FROM `{table}` WHERE {condition} = "{value}" ORDER BY {reversed} DESC'
        else:
            sql = f"SELECT * FROM `{table}` WHERE 1"

        cursor = self.connection.cursor(buffered=True)
        cursor.execute(sql)
        if rows > 1:
            records = cursor.fetchmany(rows)
        else:
            records = cursor.fetchall()

        # print(f'Total number of rows in table: {cursor.rowcount}')
        # print(f'Rows fetched: {len(records)}')

        data = []
        for row in records:
            row = list(row)
            data.append(row)

        cursor.close()
        return data

    def insertMember(self, data):
        ''' Função utilizada para inserir novo membro no banco de dados.
        DATA requer (ID, USUÁRIO, SENHA, NOME, ENDEREÇO, TIPO DE MEMBRO) '''

        try:
            sql = f"INSERT INTO Membros (ID, USUÁRIO, SENHA, NOME, UF, MEMBRO, CEP, EMAIL, TELEFONE, CELULAR, ENDERECO, NUMERO, COMPLEMENTO, BAIRRO, CIDADE, PAIS, CRM, CURRICULUM, PESSOA) VALUES ({data['id']}, '{data['usuario']}', '{data['senha']}', '{data['nome']}', '{data['uf']}', '{data['membro']}', '{data['cep']}', '{data['email']}', '{data['telefone']}', '{data['celular']}', '{data['endereco']}', '{data['numero']}', '{data['complemento']}', '{data['bairro']}', '{data['cidade']}', '{data['pais']}', '{data['crm']}', '{data['curriculum']}', '{data['pessoa']}')"
            cursor = self.connection.cursor()
            cursor.execute(sql)
        except:
            sql = f'INSERT INTO Membros (ID, USUÁRIO, SENHA, NOME, UF, MEMBRO, CEP, EMAIL, TELEFONE, CELULAR, ENDERECO, NUMERO, COMPLEMENTO, BAIRRO, CIDADE, PAIS, CRM, CURRICULUM, PESSOA) VALUES ({data["id"]}, "{data["usuario"]}", "{data["senha"]}", "{data["nome"]}", "{data["uf"]}", "{data["membro"]}", "{data["cep"]}", "{data["email"]}", "{data["telefone"]}", "{data["celular"]}", "{data["endereco"]}", "{data["numero"]}", "{data["complemento"]}", "{data["bairro"]}", "{data["cidade"]}", "{data["pais"]}", "{data["crm"]}", "{data["curriculum"]}", "{data["pessoa"]}")'
            cursor = self.connection.cursor()
            cursor.execute(sql)

        self.connection.commit()
        cursor.close()

    def insertPost(self, data):
        sql = f"INSERT INTO Blog (ID, MEMBRO, TITULO, CONTEUDO, AUTOR, DATA) VALUES {data}"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def updateTable(self, table, id, column, value, id_column):
        command = f'Update {table} set {column} = "{value}" where {id_column} = {id}'
        cursor = self.connection.cursor()
        cursor.execute(command)
        self.connection.commit()
        # cursor.close()
        print("Record Updated successfully ")
