from browser import document, ajax, html, bind, window, alert


class Member():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.uf = data['uf']
        self.cep = data['cep']
        self.member = data['member']


def showData(req):
    data = eval(req.text)
    member = Member(data)

    document['user-title'].text = 'Seus dados'
    document['user-name'].text = f'Nome: {member.name}'
    document['user-uf'].text = f'UF: {member.uf}'
    document['user-cep'].text = f'CEP: {member.cep}'
    document['user-member'].text = f'Membro: {member.member}'


def ajaxMember():
    req = ajax.Ajax()
    req.bind('complete', showData)
    req.open('POST', '/membro/', True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send({})


ajaxMember()
