from burgos.mysql_handler import Mysql
from src.config import database_auth, google_api_key
from src.mail_sender import sendMail
import json, requests

database = Mysql(database_auth, 'nada')
error = False
def start():
    database.connect()
    
    members = database.run('select * from Membros where need_location = true')
    for member in members:
        cep_str = member['cep']
        try:
            cep = int(cep_str)
            updateMember(member['id'], cep)
        except:
            continue

    if error:
        sendMail("luiz@agenciazop.com.br", "GOOGLE API precisa de pagamento", "GOOGLE API precisa de pagamento")

def getCoords(cep):
    try:
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={cep}&key={google_api_key}'
        location = json.loads(requests.get(url).text)['results'][0]['geometry']['location']
        
        return (location['lat'], location['lng'])
    except Exception as error:
        error = True
        return None

def updateMember(id, cep):
    coords = getCoords(cep)
    if coords:
        print(id, coords)
        sql = f"UPDATE Membros SET lat = {coords[0]}, lng = {coords[1]}, need_location = false WHERE id = {id}"
        database.run(sql)

start()