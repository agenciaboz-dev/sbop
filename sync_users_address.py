from src.config import database_old, database_auth
from src.mysql_handler import Mysql
import json


def collect(user, key, user_dict, old_key):
    try:
        user.update({key: str(user_dict[old_key])})
    except:
        user.update({key: None})


def capitalize_field(user, key):
    try:
        user[key] = user[key].capitalize()
    except:
        pass


old = Mysql()
old.connect(database_old)
users = []
failed = []
user_ids = []
data = old.fetchTable(0, 'sb_usermeta')

database = Mysql()
database.connect(database_auth)

for item in data:
    user_id = item[1]
    if not user_id in user_ids:
        user_ids.append(user_id)
    print(f'{data.index(item)}: {item}')

print(user_ids)
print(f'total de usuários: {len(user_ids)}')

for id in user_ids:
    user_data = old.fetchTable(0, 'sb_usermeta', 'user_id', id)
    user_dict = {}
    for item in user_data:
        user_dict.update({item[2]: item[3]})
        print(f'{user_data.index(item)}: {item[2]}: {item[3]}')

    user = {
        'usuario': user_dict['nickname'],
    }

    collect(user, 'endereco', user_dict, 'billing_address_1')
    collect(user, 'numero', user_dict, 'billing_number')
    collect(user, 'complemento', user_dict, 'billing_address_2')
    collect(user, 'bairro', user_dict, 'billing_neighborhood')


    capitalize_field(user, 'endereco')
    capitalize_field(user, 'complemento')
    capitalize_field(user, 'bairro')

    print()
    print(id)
    print(user)
    # users.append(user)
    sql = f"""UPDATE Membros SET 
            endereco='{user['endereco']}',
            numero='{user['numero']}',
            complemento='{user['complemento']}',
            bairro='{user['bairro']}'
            
            WHERE user='{user['usuario']}' ;
    """
    try:
        database.run(sql, commit=True)
    except:
        failed.append(user['usuario'])


print('-----------------')
print('failed to fix:')
for failed_user in failed:
    print(f'{user["usuario"]}')
print('-----------------')

# end of script
old.disconnect()
database.disconnect()

