from browser import document, ajax, html, bind, window, alert

jQuery = window.jQuery


class Member():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.uf = data['uf']
        self.cep = data['cep']
        self.member = data['member']


class Tool():
    def __init__(self, toolbar, content_id):
        self.toolbar = toolbar
        self.name = content_id
        self.content = document[f'{content_id}-container']

        self.toolbar.bind('click', self.switchTool)

    def switchTool(self, ev):
        alert(self.name)


def initialRender():
    jQuery('.main-container').hide()
    jQuery('#toolbar-profile').css('background-color', 'white')
    jQuery('#profile-container').show()

    for element in document.select('.toolbar'):
        tool = Tool(element, element.attrs['id'][8:])


def showData(req):
    data = eval(req.text)
    member = Member(data)

    document['user-title'].text = 'Seus dados'
    document['user-name'].text = f'Nome: {member.name}'
    document['user-uf'].text = f'UF: {member.uf}'
    document['user-cep'].text = f'CEP: {member.cep}'
    document['user-member'].text = f'Membro: {member.member}'

    initialRender()


def ajaxMember():
    req = ajax.Ajax()
    req.bind('complete', showData)
    req.open('GET', '/get_member/', True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send()


ajaxMember()
