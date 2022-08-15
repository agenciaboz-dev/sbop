from src.session_handler import Session

session = Session()

for member in session.member_list:
    try:
        session.database.updateTable(
            'Membros', member['id'], 'SENHA', member['user'], 'ID')
        print(
            f'Usuário "{member["user"]}" com senha antiga "{member["password"]}" alterada para "{member["user"]}"')
    except Exception as error:
        print(f'Erro ao atualizar senha do usuário "{member["user"]}".')
        print(error)
