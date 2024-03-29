from burgos.mysql_handler import Mysql
from src.config import database_auth, google_api_key
import json, requests

database = Mysql(database_auth, 'nada')
def start():
    database.connect()
    
    members = database.run('select * from Membros')
    for member in members:
        cep_str = member['CEP']
        try:
            cep = int(cep_str)
            updateMember(member['ID'], cep)
        except:
            continue

def getCoords(cep):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={cep}&key={google_api_key}'
    location = json.loads(requests.get(url).text)['results'][0]['geometry']['location']
    
    return (location['lat'], location['lng'])

def updateMember(id, cep):
    coords = getCoords(cep)
    print(id, coords)
    sql = f"UPDATE Membros SET lat = {coords[0]}, lng = {coords[1]} WHERE ID = {id}"
    database.run(sql)

start()