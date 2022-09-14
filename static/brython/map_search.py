from browser import document, ajax, html, bind, window, aio

jQuery = window.jQuery
tooltip = jQuery("#map-tooltip")
member_tooltip = document['member-tooltip']
members = []


def slowIncreaseTo(element, n):
    aio.sleep()


def initialRender(req):
    data = eval(req.text)
    document['map-status-medicos'].text = data['medicos']
    document['map-status-estados'].text = data['estados']
    document['map-status-cidades'].text = data['cidades']

    def renderMap():
        jQuery('.body-wrapper').fadeIn('slow')

    jQuery('#member-tooltip').hide()
    jQuery('#loading-screen').fadeOut(renderMap)


class Member():
    def __init__(self, data):
        self.id = data['id']
        self.img = None
        self.name = data['name']
        self.telefone = data['telefone']
        self.email = data['email']
        self.endereco = data['endereco']
        self.numero = data['numero']
        self.complemento = data['complemento']
        self.cep = data['cep']
        self.cidade = data['cidade']
        self.uf = data['uf']
        self.crm = data['crm']
        self.curriculum = data['curriculum']

        self.member_container_wrapper = None
        self.container = None
        self.data_container = None
        self.clicked = False
        self.endereco_formatado = None

        self.printResult()
        self.container.bind('click', self.tooltipHandler)

    def printResult(self):
        member_container_wrapper = html.DIV(
            '', Class="result member-container-wrapper")
        document['result'] <= member_container_wrapper
        self.member_container_wrapper = member_container_wrapper

        # defining a member container
        container = html.DIV(
            '', Id=f'container-medico-{self.id}', Class='result member-container')
        member_container_wrapper <= container
        self.container = container

        # importing image
        doctor_icon = html.IMG(
            '', Src='/static/image/doctor_icon.svg', Alt='Doctor Icon', Class='result doctor-icon')
        container <= doctor_icon

        # defining a data container
        data_container = html.DIV(
            '', Id=f'data-container-medico-{self.id}', Class='result member-data-container')
        container <= data_container
        self.data_container = data_container

        # adding name to DOM
        element = html.P(
            f'Nome: {self.name}', Id=f'medico-{self.id}', Class='result member-name')
        data_container <= element

        # adding phone to DOM
        telefone = self.telefone
        telefone = f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
        self.telefone = telefone
        element = html.P(
            f'Contato: {telefone} | {self.email}', Class='result')
        data_container <= element

        # formating and adding address to DOM
        endereco = f'{self.endereco}, {self.numero} | {self.complemento}'
        self.endereco_formatado = endereco
        element = html.P(f'Endereço: {endereco}', Class='result')
        data_container <= element

        # formating cep string and adding to DOM
        cep = self.cep[:-3]+"-"+self.cep[-3:]
        element = html.P(
            f'Cidade: {self.cidade} - {self.uf} | CEP: {cep}', Class='result')
        data_container <= element

        # adding line in end of container
        line = html.HR('', Class='result dividing-line')
        member_container_wrapper <= line

    def tooltipHandler(self, ev):
        if not self.clicked:
            for item in members:
                item.clicked = False
            self.clicked = True

            jQuery('#member-tooltip').fadeIn()
            member_tooltip.left = document['result'].abs_left + \
                document['result'].width + 25
            member_tooltip.top = document['result'].abs_top

            tooltip_arrow = jQuery('#member-tooltip::before')

            jQuery('#tooltip-nome').text(self.name)
            jQuery('#tooltip-especialidade>span').text('Sem dados')
            jQuery('#tooltip-crm>span').text(self.crm)
            jQuery('#tooltip-contato>span').text(self.telefone)
            jQuery('#tooltip-email>span').text(self.email)
            jQuery('#tooltip-endereco>span').text(self.endereco_formatado)

            jQuery('#tooltip-curriculum').text(self.curriculum)
        else:
            self.clicked = False
            jQuery('#member-tooltip').fadeOut()


def showResult(req):
    member_list = eval(req.text)
    title = member_list.pop(0).upper()
    document['search-title'].text = 'Resultados para: '
    document['searched-value'].text = title
    if member_list:
        for item in member_list:
            member = Member(item)
            members.append(member)

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


def ajaxEstados():
    req = ajax.Ajax()
    req.bind('complete', estadosData)
    req.open('GET', '/estados_data/', True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send({})


def clearResult(idle=False):
    def statusFadeOut():
        document['search-title'].text = 'Pesquisando'
        jQuery('.reset-button-wrapper').fadeIn()
        document['search-result'].style.display = 'flex'
        document['search-result'].style.visibility = 'visible'

    def statusFadeIn():
        jQuery("#map-status").fadeIn()

    if idle:
        jQuery('.reset-button-wrapper').fadeOut(statusFadeIn)
        jQuery('#search-result').fadeOut()
        document['searched-value'].text = ''
        document['search-title'].text = ''
    else:
        document['searched-value'].text = ''
        document['search-title'].text = ''

        jQuery("#map-status").fadeOut(statusFadeOut)

    jQuery('#member-tooltip').fadeOut()
    jQuery(".result").remove()

    document['name-search-input'].value = ''
    document['cep-search-input'].value = ''


class Estado():
    def __init__(self, uf, element, name, count):
        self.uf = uf
        self.id = f'#estado-{uf}'
        self.name = name
        self.count = count
        self.element = element
        self.left = self.element.abs_left
        self.top = self.element.abs_top

        @bind(self.id, 'click')
        def searchMap(ev):

            data = {
                'search': 'uf',
                'value': uf
            }
            document['search-title'].text = 'Pesquisando'
            clearResult()
            ajaxSearch(data)

        @bind(self.id, 'mouseenter')
        def mapTooltipIn(ev):
            global tooltip
            uf = jQuery(self.id)
            targetOffset = uf.offset()
            print(targetOffset.left, targetOffset.top)

            if not self.uf == 'rs' and not self.uf == 'sc':
                tooltip.css('left', f'{int(targetOffset.left + uf.width()/2)}px')
                tooltip.css('transform', 'translateX(-50%)')
                tooltip.css('top', f'{int(targetOffset.top + uf.height()/2) + 20}px')
            else:
                tooltip.css('left', f'{int(jQuery(".body-wrapper").width())}px')
                tooltip.css('top', f'{int(jQuery(".body-wrapper").height())}px')
                tooltip.css('transform', 'translateX(-100%) translateY(-62%)')

            jQuery('#map-tooltip>div>p').text(self.name)

            if self.count == 0:
                jQuery('#map-tooltip>div>div>p').text('')
                jQuery(
                    '#map-tooltip>div>div>p').append('<span></span> médico cadastrado em nosso sistema')
                jQuery('#map-tooltip>div>div>p>span').text('Nenhum')

            elif self.count == 1:
                jQuery('#map-tooltip>div>div>p').text('')
                jQuery(
                    '#map-tooltip>div>div>p').append('<span></span> médico cadastrado em nosso sistema')
                jQuery('#map-tooltip>div>div>p>span').text(self.count)

            else:
                jQuery('#map-tooltip>div>div>p').text('')
                jQuery(
                    '#map-tooltip>div>div>p').append('<span></span> médicos cadastrados em nosso sistema')
                jQuery('#map-tooltip>div>div>p>span').text(self.count)

            tooltip.show()

        @bind(self.id, 'mouseleave')
        def mapTooltipOut(ev):
            tooltip.hide()


def estadosData(req):
    estados = eval(req.text)
    for estado in document.select('.estado'):
        uf = estado.attrs['id'][7:]
        name = estado.attrs['name']
        count = estados.count(uf)
        estado_ = Estado(uf, estado, name, count)


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


@bind('#map-tooltip', 'mouseenter')
def mapTooltipIn_(ev):
    ev.preventDefault()
    print(f'mouse em cima da tooltip')
    jQuery('#map-tooltip').show()


@bind('#map-tooltip', 'mouseleave')
def mapTooltipIn_(ev):
    tooltip.hide()


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
ajaxEstados()
