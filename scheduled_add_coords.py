from burgos.mysql_handler import Mysql
from src.config import database_auth, google_api_key
from src.mail_sender import sendMail
import json, requests

database = Mysql(database_auth, 'nada')
error = []
def start():
    database.connect()
    
    members = database.run('select * from Membros where need_location = true')
    for member in members:
        cep_str = member['cep']
        try:
            cep = int(cep_str)
            updateMember(member, cep)
        except:
            continue

    if error:
        sendMail("luiz@agenciazop.com.br", "GOOGLE API precisa de pagamento", f"Olá, não foi possível validar algum(ns) endereço(s) no sistema devido a um erro nas requisições do Google Maps API.\nCadastros com erro:\n{error}")

def getCoords(cep):
    try:
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={cep}&key={google_api_key}'
        location = json.loads(requests.get(url).text)['results'][0]['geometry']['location']
        
        return (location['lat'], location['lng'])
    except Exception as error:
        return None

def updateMember(member, cep):
    global error
    id = member['id']
    coords = getCoords(cep)
    if coords:
        print(id, coords)
        sql = f"UPDATE Membros SET lat = {coords[0]}, lng = {coords[1]}, need_location = false WHERE id = {id}"
        database.run(sql)
    else:
        error.append(member['nome'])

start()