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
            member_container_wrapper = html.DIV(
                '', Class="result member-container-wrapper")
            document['result'] <= member_container_wrapper

            # defining a member container
            container = html.DIV(
                '', Id=f'container-medico-{member["id"]}', Class='result member-container')
            member_container_wrapper <= container

            # importing image
            doctor_icon = html.IMG(
                '', Src='/static/image/doctor_icon.svg', Alt='Doctor Icon', Class='result doctor-icon')
            container <= doctor_icon

            # defining a data container
            data_container = html.DIV(
                '', Id=f'data-container-medico-{member["id"]}', Class='result member-data-container')
            container <= data_container

            # adding name to DOM
            element = html.P(
                f'Nome: {member["name"]}', Id=f'medico-{member["id"]}', Class='result')
            data_container <= element

            # adding phone to DOM
            telefone = member["telefone"]
            telefone = f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
            element = html.P(
                f'Contato: {telefone} | {member["email"]}', Class='result')
            data_container <= element

            # formating and adding address to DOM
            endereco = f'{member["cidade"]} | {member["endereco"]}, {member["numero"]} | {member["complemento"]}'
            element = html.P(f'Endereço: {endereco}', Class='result')
            data_container <= element

            # formating cep string and adding to DOM
            cep = member["cep"][:-3]+"-"+member["cep"][-3:]
            element = html.P(f'CEP: {cep}', Class='result')
            data_container <= element

            # adding line in end of container
            line = html.HR('', Class='result dividing-line')
            member_container_wrapper <= line

    else:
        document['result'] <= html.P('Nenhum resultado', Class='result')

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
        document['search-result'].style.display = 'none'
        document['search-result'].style.visibility = 'none'
        document['reset-button'].style.display = 'none'
        document['reset-button'].style.visibility = 'none'
        document['searched-value'].text = ''
        document['search-title'].text = ''
    else:
        document['map-status'].style.display = 'none'
        document['map-status'].style.visibility = 'none'
        document['search-result'].style.display = 'flex'
        document['search-result'].style.visibility = 'visible'
        document['reset-button'].style.display = 'flex'
        document['reset-button'].style.visibility = 'visible'
        document['searched-value'].text = ''
        document['search-title'].text = 'Pesquisando'

    for element in document.select(".result"):
        element.style.display = 'none'
        element.style.visibility = 'none'

    document['name-search-input'].value = ''
    document['cep-search-input'].value = ''


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

document
ajaxPreLoad()
