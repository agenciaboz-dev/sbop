from browser import document, ajax, html, bind, window, alert


def showResult(req):
    member_list = eval(req.text)
    document['searching'].text = ''
    container = document['result']
    if member_list:
        for member in member_list:
            # adding name to DOM
            element = html.P(
                f'Nome: {member["name"]}', Id=f'medico-{member["id"]}', Class='result')
            container <= element

            # adding UF to DOM
            element = html.P(f'UF: {member["uf"]}', Class='result')
            container <= element

            # formatting cep string
            cep = member["cep"][:-3]+"-"+member["cep"][-3:]
            # adding cep to DOM
            element = html.P(f'CEP: {cep}', Class='result')
            element.style.margin = '5px 5px 25px 5px'
            container <= element

    else:
        container <= html.P('Médico não encontrado', Class='result')


def ajaxSearch(data):
    req = ajax.Ajax()
    req.bind('complete', showResult)
    req.open('POST', '/membros/', True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send(data)


def clearResult():
    for element in document.select(".result"):
        element.style.display = 'none'
        element.style.visibility = 'none'


@bind('#name-search-form', 'submit')
def nameSearch(ev):
    clearResult()
    ev.preventDefault()
    input = document["name-search-input"]
    input.blur()
    data = {
        'search': 'name',
        'name': input.value
    }
    document['searching'].text = 'Pesquisando'
    ajaxSearch(data)


@bind('#cep-search-form', 'submit')
def nameSearch(ev):
    clearResult()
    ev.preventDefault()
    input = document["cep-search-input"]
    input.blur()
    data = {
        'search': 'cep',
        'cep': input.value
    }
    document['searching'].text = 'Pesquisando'
    ajaxSearch(data)
