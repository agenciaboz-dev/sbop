from src.session_handler import Session
from src.config import database_old
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


def numerize_phones(user):
    try:
        user['telefone'] = user['telefone'].replace(
            ')', '').replace('(', '').replace(' ', '').replace('-', '')
    except:
        pass

    try:
        user['celular'] = user['celular'].replace(
            ')', '').replace('(', '').replace(' ', '').replace('-', '')
    except:
        pass


old = Mysql()
old.connect(database_old)
session = Session()
users = []
user_ids = []
data = old.fetchTable(0, 'sb_usermeta')

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
        'senha': None,
    }
    if user_dict['first_name']:
        if user_dict['last_name']:
            nome = (user_dict['first_name'] + ' ' +
                    user_dict['last_name']).lower().title()
        else:
            nome = user_dict['first_name'].lower().title()
    else:
        nome = None
    user.update({'nome': nome})

    collect(user, 'email', user_dict, 'billing_email')
    collect(user, 'telefone', user_dict, 'billing_phone')
    collect(user, 'celular', user_dict, 'billing_cellphone')
    collect(user, 'pessoa', user_dict, 'billing_persontype')
    collect(user, 'endereco', user_dict, 'billing_address_1')
    collect(user, 'numero', user_dict, 'billing_number')
    collect(user, 'complemento', user_dict, 'billing_address_2')
    collect(user, 'bairro', user_dict, 'billing_neighborhood')
    collect(user, 'cidade', user_dict, 'billing_city')
    collect(user, 'uf', user_dict, 'billing_state')
    collect(user, 'pais', user_dict, 'billing_country')
    collect(user, 'cep', user_dict, 'billing_postcode')
    collect(user, 'crm', user_dict, 'billing_crm')
    collect(user, 'curriculum', user_dict, 'billing_mini_curriculum')
    collect(user, 'membro', user_dict, 'tipo_cliente')

    # formatting data
    try:
        if user['membro'] == 'Assinante':
            user['membro'] = 'Associado'
    except:
        pass

    try:
        user['email'] = user['email'].lower()
    except:
        pass

    capitalize_field(user, 'endereco')
    capitalize_field(user, 'complemento')
    capitalize_field(user, 'bairro')
    capitalize_field(user, 'cidade')

    numerize_phones(user)

    try:
        user['cep'] = user['cep'].replace('-', '')
    except:
        pass

    print()
    print(id)
    print(user)
    # users.append(user)
    feedback, sidgnedup = session.signup(user)
    print(feedback)


# end of script
old.disconnect()
session.database.disconnect()
