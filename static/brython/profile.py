from browser import document, ajax, html, bind, window, alert, timer

jQuery = window.jQuery


class Member():
    def __init__(self, data):
        self.id = data['id']
        self.username = data['user']
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
        self.type = data['member']

        self.member_container_wrapper = None
        self.container = None
        self.data_container = None
        self.clicked = False
        self.endereco_formatado = None

        telefone = f"({self.telefone[:2]}) {self.telefone[2:7]}-{self.telefone[7:]}"
        self.telefone = telefone
        endereco = f'{self.endereco}, {self.numero} | {self.complemento}'
        self.endereco_formatado = endereco


class Tool():
    def __init__(self, toolbar, content_id):
        self.toolbar = toolbar
        self.name = content_id
        self.content_id = f'{content_id}-container'
        self.content = document[f'{content_id}-container']

        self.toolbar.bind('click', self.switchTool)

    def activateScreen(self):
        jQuery(self.toolbar).addClass('toolbar-active')
        jQuery(self.content).fadeIn()
        # timer.set_timeout(, 500)

    def switchTool(self, ev):
        if not self.content.style.display == 'none':
            return None

        jQuery('.main-container').hide()
        jQuery('.toolbar').removeClass('toolbar-active')

        jQuery(self.toolbar).addClass('toolbar-active')
        jQuery(self.content).fadeToggle('slow')


def initialRender():
    jQuery('.main-container').hide()
    jQuery('#toolbar-profile').addClass('toolbar-active')
    jQuery('#profile-container').show()

    for element in document.select('.toolbar'):
        tool = Tool(element, element.attrs['id'][8:])

    jQuery('#loading-screen').slideToggle('slow')


def loadActivePlan(member):
    member_type = f'#{member.type.lower()}'
    jQuery(member_type).addClass('active-plan')

    # icon
    icon = html.IMG('', Id='active-plan-icon',
                    Src='/static/image/active-plan-icon.svg')
    document[member_type[1:]] <= icon
    height = jQuery(member_type).height()
    jQuery(icon).css('transform', f'translateY({height/4}px)')

    # text
    vigente = ''
    jQuery('.active-plan > .plan-title').append('<p>Plano Atual</p>')
    jQuery('.active-plan > .plan-title > p').css('color', 'var(--primary-color)')


def loadProfile(member):
    document['data-name'].text = member.name
    document['data-crm'].text = member.crm
    document['data-phone'].text = member.telefone
    document['data-address'].text = member.endereco_formatado
    document['data-username'].text = member.username
    document['data-specialization'].text = 'Sem dados'
    document['data-email'].text = member.email
    document['data-curriculum'].text = member.curriculum


def preLoad(req):
    data = eval(req.text)
    member = Member(data)

    loadProfile(member)
    loadActivePlan(member)
    initialRender()


def ajaxMember():
    req = ajax.Ajax()
    req.bind('complete', preLoad)
    req.open('GET', '/get_member/', True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send()


@bind('#camera-icon-container', 'click')
def uploadPicture(ev):
    alert('caixa de diálogo pra upload de foto')


ajaxMember()
