from browser import document, ajax, html, bind, window, alert


def initialRender(req):
    data = eval(req.text)
    document['map-status-medicos'].text = data['medicos']
    document['map-status-estados'].text = data['estados']
    document['map-status-cidades'].text = data['cidades']


def showResult(req):
    member_list = eval(req.text)
    title = member_list.pop(0).upper()
    document['search-title'].text = 'Resultados para: '
    document['searched-value'].text = title
    if member_list:
        for member in member_list:
            # defining a member container
            container = html.DIV(
                '', Id=f'container-medico-{member["id"]}', Class='result member-container')
            document['result'] <= container

            # adding name to DOM
            element = html.P(
                f'Nome: {member["name"]}', Id=f'medico-{member["id"]}', Class='result')
            container <= element

            # adding UF to DOM
            element = html.P(f'UF: {member["uf"]}', Class='result')
            container <= element

            element = html.P(f'Cidade: {member["cidade"]}', Class='result')
            container <= element

            # formatting cep string
            cep = member["cep"][:-3]+"-"+member["cep"][-3:]
            # adding cep to DOM
            element = html.P(f'CEP: {cep}', Class='result')
            element.style.margin = '5px 5px 25px 5px'
            container <= element

    else:
        container <= html.P('Médico não encontrado', Class='result')

    container <= html.BUTTON('Reset', Id='reset-button', Class='result')

    @bind('#reset-button', 'click')
    def resetResult(ev):
        clearResult(idle=True)


def ajaxSearch(data):
    req = ajax.Ajax()
    req.bind('complete', showResult)
    req.open('POST', '/membros/', True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send(data)


def ajaxPreLoad():
    req = ajax.Ajax()
    req.bind('complete', initialRender)
    req.open('GET', '/get_map_status/', True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send({})


def clearResult(idle=False):
    if idle:
        document['map-status'].style.display = 'flex'
        document['map-status'].style.visibility = 'visible'
    else:
        document['map-status'].style.display = 'none'
        document['map-status'].style.visibility = 'none'

    for element in document.select(".result"):
        element.style.display = 'none'
        element.style.visibility = 'none'

    document['name-search-input'].value = ''
    document['cep-search-input'].value = ''
    document['search-title'].text = ''
    document['searched-value'].text = ''


class Estado():
    def __init__(self, uf):
        self.uf = uf
        self.id = f'#estado-{uf}'

        @bind(self.id, 'click')
        def searchMap(ev):

            data = {
                'search': 'uf',
                'value': uf
            }
            document['search-title'].text = 'Pesquisando'
            clearResult()
            ajaxSearch(data)


for estado in document.select('.estado'):
    uf = estado.attrs['id'][7:]
    estado_ = Estado(uf)


@bind('#name-search-form', 'submit')
def nameSearch(ev):
    ev.preventDefault()
    input = document["name-search-input"]
    input.blur()
    data = {
        'search': 'name',
        'value': input.value
    }
    document['search-title'].text = 'Pesquisando'
    clearResult()
    ajaxSearch(data)


@bind('#cep-search-form', 'submit')
def nameSearch(ev):
    ev.preventDefault()
    input = document["cep-search-input"]
    input.blur()
    cep = input.value.replace('-', '')
    # removing hyphen from text
    # cep = cep[:5] + cep[-3:]
    data = {
        'search': 'cep',
        'value': cep
    }
    document['search-title'].text = 'Pesquisando'
    clearResult()
    ajaxSearch(data)


# @bind('#cep-search-input', 'input')
# def cep(ev):
#     element = document['cep-search-input']
#     try:
#         int(element.value[-1:])
#         if len(element.value) == 5:
#             element.value += '-'
#     except:
#         element.value = element.value[:-1]


ajaxPreLoad()
