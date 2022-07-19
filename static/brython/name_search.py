from browser import document, ajax, html, bind, window, alert


def showResult(req):
    member = eval(req.text)
    container = document['name-feedback']
    if member:
        element = html.P(
            f'Nome: {member["name"]}', Id=f'medico-{member["id"]}', Class='result')
        container <= element

        element = html.P(f'UF: {member["uf"]}', Class='result')
        container <= element
    else:
        container <= html.P('Médico não encontrado', Class='result')


def ajaxNameSearch(data):
    req = ajax.Ajax()
    req.bind('complete', showResult)
    req.open('POST', '/membros/', True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send(data)


@bind('#name-search-button', 'click')
def nameSearch(ev):
    data = {
        'search': 'name',
        'name': document["name-search-form"].value
    }
    for element in document.select(".result"):
        element.style.display = 'none'
        element.style.visibility = 'none'
    ajaxNameSearch(data)
