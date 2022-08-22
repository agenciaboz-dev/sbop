from browser import document, ajax, html, bind, window, alert, timer

jQuery = window.jQuery
member = []
selected_plan = None
POPUP = jQuery('#floating-popup')
container_height = jQuery('#profile-container').height()
container_width = jQuery('#profile-container').width()


class Member():
    def __init__(self, data):
        self.id = data['id']
        self.cpf = data['cpf']
        self.username = data['user']
        self.password = data['password']
        self.img = None
        self.name = data['name']
        self.telefone = data['telefone']
        self.telefone_plain = data['telefone']
        self.email = data['email']
        self.endereco = data['endereco']
        self.rua = data['endereco']
        self.bairro = data['bairro']
        self.numero = data['numero']
        self.complemento = data['complemento']
        self.cep = data['cep']
        self.cidade = data['cidade']
        self.uf = data['uf']
        self.crm = data['crm']
        self.curriculum = data['curriculum']
        self.type = data['member']
        self.solicitacoes = data['solicitacoes']
        self.especialidades = data['especialidades']
        self.especialidades_str = None
        self.temporario = eval(data['temporario'])
        self.primeiro_acesso = eval(data['primeiro_acesso'])
        self.pago = eval(data['pago'])

        self.member_container_wrapper = None
        self.container = None
        self.data_container = None
        self.clicked = False
        self.endereco_formatado = None

        telefone = f"({self.telefone[:2]}) {self.telefone[2:7]}-{self.telefone[7:]}"
        self.telefone = telefone
        endereco = f'{self.endereco}, {self.numero} | {self.complemento}'
        self.endereco_formatado = endereco

    def updatePassword(self):
        POPUP.fadeToggle()
        POPUP.find('h1').text('Atualize sua senha')
        POPUP.find('p').text(
            'O sistema foi atualizado e sua senha precisa ser redefinida.')

        pass_input = '<label for="input-new-password-temp">Nova senha</label><input type="password" id="input-new-password-temp" required>'
        pass_input_confirmation = '<label for="input-new-password-temp-conf">Confirme a nova senha</label><input type="password" id="input-new-password-temp-conf" required>'
        button = POPUP.find('button')
        button.remove()
        POPUP.append(pass_input)
        POPUP.append(pass_input_confirmation)
        POPUP.append(button)
        resizePopUp(height_factor=3.5)
        POPUP.css('transform',
                  f'translateY({container_height/4}px) translateX({container_width/3}px)')

        def updatePasswordButton(ev):
            print('atualizar senha')

            new_password = jQuery('#input-new-password-temp')
            new_password_conf = jQuery('#input-new-password-temp-conf')
            if new_password.val():
                if new_password.val() == new_password_conf.val():
                    def onCompletePasswordUpdate(req):
                        toggleContainer(selection=['#temporary-container'])
                        POPUP.fadeToggle()
                        toggleContainer(selection=['.main-container'])
                        POPUP.find('button').off('click')
                        POPUP.find('button').on('click', togglePopUp)
                        # alert(eval(req.text)[0])

                    data = {
                        'id': member.id,
                        'new_password': new_password.val(),
                        'first_access': True
                    }

                    _ajax('/change_password/', onCompletePasswordUpdate,
                          method='POST', data=data)
                else:
                    POPUP.find('p').text(
                        'Senhas não conferem. Por favor, tente novamente.')
                    new_password.val('')
                    new_password_conf.val('')
                    new_password.focus()
            else:
                POPUP.find('p').text('Insira uma senha')

        POPUP.find('button').off('click')
        POPUP.find('button').on('click', updatePasswordButton)


class Tool():
    def __init__(self, toolbar, content_id):
        self.toolbar = toolbar
        self.name = content_id
        self.content_id = f'{content_id}-container'
        self.content = document[f'{content_id}-container']

        self.toolbar.bind('click', self.switchTool)

    def switchTool(self, ev):
        if not self.content.style.display == 'none':
            return None

        jQuery('.main-container').hide()
        jQuery('.toolbar').removeClass('toolbar-active')

        jQuery(self.toolbar).addClass('toolbar-active')
        jQuery(self.content).fadeToggle('slow')

        # reset selected plan
        if member.pago:
            jQuery('.selected-plan').removeClass('selected-plan')
            jQuery('#plans-container > button').addClass('deactivated-button')


class RestrictTool():
    def __init__(self, element, content_id):
        self.toolbar = element
        self.name = content_id
        self.content_id = f'{content_id}-container'
        self.content = document[self.content_id]

        print(self.name, self.content_id)

        self.toolbar.bind('click', self.switchTool)

    def switchTool(self, ev):
        if not self.content.style.display == 'none':
            return None

        jQuery('.restrict-content').hide()
        jQuery('.restrict-toolbar > h1').removeClass('active-restrict-tool')

        jQuery(self.toolbar).addClass('active-restrict-tool')
        jQuery(self.content).fadeToggle('slow')


class Plan():
    def __init__(self, element):
        self.element = element
        self.name = self.element.attrs['id']

        if member.pago:
            self.element.bind('click', self.selectPlan)

    def selectPlan(self, ev):
        global selected_plan
        jQuery('.selected-plan').removeClass('selected-plan')

        if self.name == member.type.lower():
            jQuery('#plans-container > button').addClass('deactivated-button')
            selected_plan = None
            return None

        jQuery(self.element).addClass('selected-plan')
        jQuery('#plans-container > button').removeClass('deactivated-button')
        selected_plan = self


def toggleContainer(selection=['.main-container', '.body-toolbar'], mode=None):
    if mode == 'blur':
        for item in selection:
            jQuery(item).css('opacity', '0.5')
            # jQuery(item).css('filter', 'blur(2px)')
            jQuery(item).css('pointer-events', 'none')
    else:
        for item in selection:
            jQuery(item).css('opacity', '1')
            # jQuery(item).css('filter', 'blur(0)')
            jQuery(item).css('pointer-events', 'auto')


def addVideo(src):
    video_wrapper = html.DIV('', Class='video-wrapper')
    jQuery('#videos-container').append(video_wrapper)

    video = f'<video controls controlsList="nodownload" disablePictureInPicture id="video" width="400" height="200" src="/static/videos/{member.type}/{src}"></video>'
    jQuery(video_wrapper).append(video)

    video_text_container = html.DIV('', Class='video-text-container')
    jQuery(video_wrapper).append(video_text_container)

    title = f'<h1>{src.split(".")[0]}</h1>'
    description = f'<p>balbalblalbalbalbal</p>'
    jQuery(video_text_container).append(title)
    jQuery(video_text_container).append(description)

    jQuery('#videos-container').append('<hr>')


def videosList(req):
    videos = eval(req.text)
    print(videos)
    if not videos:
        return None
    for item in videos:
        addVideo(item)


def addRestrictContent(post):
    restrict_content_wrapper = html.DIV('', Class='restrict-content-wrapper')
    jQuery('#publicacoes-container').append(restrict_content_wrapper)

    img = f'<img width="400" height="200" src="/static/posts/img.png" alt"imagem"></img>'
    jQuery(restrict_content_wrapper).append(img)

    restrict_content_text_container = html.DIV(
        '', Class='restrict-content-text-container')
    jQuery(restrict_content_wrapper).append(restrict_content_text_container)

    title = f'<h1>{post[2]}</h1>'
    autor = html.P(f'{post[4]} - {post[5]}', Class='restrict-content-author')
    description = f'<p>{post[3]}</p>'
    jQuery(restrict_content_text_container).append(title)
    jQuery(restrict_content_text_container).append(autor)
    jQuery(restrict_content_text_container).append(description)

    jQuery('#publicacoes-container').append('<hr>')


def restrictContentList(req):
    data = eval(req.text)
    data.reverse()

    for post in data:
        addRestrictContent(post)


def resizePopUp(width_factor=1, height_factor=3.5, translate_factor=1.75/2):
    jQuery('#floating-popup').height(jQuery('#floating-popup').height() * height_factor)


def togglePopUp(ev):
    POPUP.fadeToggle()
    toggleContainer()

    # remove inputs
    POPUP.find('input').fadeOut()
    POPUP.find('label').fadeOut()


def renderPopUp():
    POPUP.css('transform',
              f'translateY({container_height/2}px) translateX({container_width/3}px)')

    POPUP.fadeToggle()

    POPUP.find('button').on('click', togglePopUp)


def initialRender():
    jQuery('#temporary-container').hide()
    jQuery('.main-container').hide()
    jQuery('.stages-container').hide()
    jQuery('#toolbar-profile').addClass('toolbar-active')
    jQuery('#profile-container').show()
    jQuery('textarea').hide()
    

    for element in document.select('.toolbar'):
        tool = Tool(element, element.attrs['id'][8:])

    renderPopUp()

    jQuery('#loading-screen').slideToggle('slow')

    if member.primeiro_acesso:
        toggleContainer(selection=['#temporary-container'], mode='blur')
        member.updatePassword()

    if member.temporario:
        jQuery('.main-container').hide()
        toggleContainer(selection=['.body-toolbar'], mode='blur')
        jQuery('#temporary-container').show()
        jQuery('#stage-1-button').on('click', renderStage1)
        
        if member.type:
            jQuery('.temporary-stage-2').find('img').attr('src','/static/image/complete_icon.svg')


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
    jQuery('.active-plan > .plan-title').append('<p>Plano Atual. Vigente até 31/12/2012</p>')
    jQuery('.active-plan > .plan-title > p').css('color', 'var(--primary-color)')

    # checar vencimento
    if not member.pago:
        jQuery('.active-plan').css('outline-color', 'var(--borda-plano-vencido)')
        jQuery('#active-plan-icon').attr('src', '/static/image/alert.svg')
        jQuery('.active-plan > .plan-title > p').text('Plano Atual.')
        jQuery('.active-plan > .plan-title > p').append('<span>Pagamento do dia 31/12/2022 atrasado!</span>')
        jQuery('.active-plan > .plan-title > p > span').css('color', 'var(--borda-plano-vencido)')
        jQuery('.active-plan > .plan-title > p > span').css('font-weight', 'bold')

        jQuery('.plans:not(.active-plan)').css('cursor', 'not-allowed')
        jQuery('.active-plan').css('cursor', 'auto')

        jQuery('#plans-container > button').removeClass('deactivated-button')
        jQuery('#plans-container > button').addClass('regularize-button')
        jQuery('#plans-container > button').text('Regularize Já!')
        
    else:
        jQuery('#toolbar-plans > img').hide()
        

    # iterate plans divs
    for element in document.select('.plans'):
        plan = Plan(element)

    @bind('#plans-container > button', 'click')
    def ajaxPlan(ev):
        req = ajax.Ajax()
        req.bind('complete', changePlanFeedback)
        req.open('POST', '/change_plan/', True)
        req.set_header('content-type', 'application/x-www-form-urlencoded')
        req.send({'id': member.id, 'plan': selected_plan.name})

    def changePlanFeedback(req):
        jQuery('.selected-plan').removeClass('selected-plan')
        jQuery('#plans-container > button').addClass('deactivated-button')
        alert('seguir pro pagamento?')


def renderStage1(ev):
    jQuery('.temporary-stages').fadeOut(jQuery('.stage-1-container').fadeIn)
    jQuery('#submit-stage-1-button').on('click', renderStage2)
    
    jQuery('#member-input-name').val(member.name)
    jQuery('#member-input-cpf').val(member.cpf)
    jQuery('#member-input-telefone').val(member.telefone)
    jQuery('#member-input-email').val(member.email)
    jQuery('#member-input-crm').val(member.crm)
    jQuery('#member-input-curriculum').val(member.curriculum)
    jQuery('#member-input-cep').val(member.cep)
    jQuery('#member-input-endereco').val(member.rua)
    jQuery('#member-input-numero').val(member.numero)
    jQuery('#member-input-complemento').val(member.complemento)
    jQuery('#member-input-bairro').val(member.bairro)
    jQuery('#member-input-cidade').val(member.cidade)
    jQuery('#member-input-uf').val(member.uf)
    
    print(member.especialidades)
    for element in document.select('.checkbox'):
        if element.attrs['value'] in member.especialidades:
            element.checked = True
    
    
    
def renderStage2(ev):
    if not jQuery('#member-input-cpf').val():
        alert('Insira um CPF')
        return None
    
    if not len(jQuery('#member-input-cpf').val()) == 11:
        alert('CPF inválido')
        jQuery('#member-input-cpf').val('')
        jQuery('#member-input-cpf').focus()
        return None
    
    member.especialidades = []
    for element in document.select('.checkbox'):
        if element.checked:
            member.especialidades.append(element.attrs['value'])
    
    especialidades = ''
    for item in member.especialidades:
        especialidades += item+','
    member.especialidades_str = especialidades.strip(',')
            
    member.name = jQuery('#member-input-name').val()
    member.cpf = jQuery('#member-input-cpf').val()
    member.telefone = jQuery('#member-input-telefone').val()
    member.email = jQuery('#member-input-email').val()
    member.crm = jQuery('#member-input-crm').val()
    member.curriculum = jQuery('#member-input-curriculum').val()
    member.cep = jQuery('#member-input-cep').val()
    member.rua = jQuery('#member-input-endereco').val()
    member.numero = jQuery('#member-input-numero').val()
    member.complemento = jQuery('#member-input-complemento').val()
    member.bairro = jQuery('#member-input-bairro').val()
    member.cidade = jQuery('#member-input-cidade').val()
    member.uf = jQuery('#member-input-uf').val()
    
    def updateProfileComplete(req):
        response = eval(req.text)
        if response:
            # removing button from stage-1
            jQuery('.temporary-stage-1').find('button').remove()
            # appending img to stage-1
            img = '<img src="/static/image/complete_icon.svg" alt="">'
            jQuery('.temporary-stage-1').append(img)
            
            if member.type:
                jQuery('.temporary-stage-3').find('img').remove()
                button = html.BUTTON('Finalizar', Id='finish-temporary-profile-button')
                jQuery('.temporary-stage-3').append(button)
                def removeTemporary(ev):
                    # toggleContainer()
                    # jQuery('#temporary-container').fadeOut(jQuery('#profile-container').fadeIn)
                    # loadMember()
                    def reloadPage(req):
                        window.location.href = '/home/'
                        
                    _ajax('/remove_temporary/', reloadPage, method='POST', data={'id': member.id})

                jQuery(button).on('click', removeTemporary)
            else:
                jQuery('.temporary-stage-2').find('img').remove()
                button = html.BUTTON('Prosseguir', Id='stage-2-button')
                jQuery('.temporary-stage-2').append(button)
            
            
            jQuery('.stage-1-container').fadeOut(jQuery('.temporary-stages').fadeIn)
    
    _ajax('/update_profile/', updateProfileComplete, method='POST', data=vars(member))
    
    

def loadProfile():
    document['data-name'].text = member.name
    document['data-crm'].text = member.crm
    document['data-phone'].text = member.telefone
    document['data-address'].text = member.endereco_formatado
    document['data-username'].text = member.username
    document['data-email'].text = member.email
    document['data-curriculum'].text = member.curriculum

    especialidades = ''
    for item in member.especialidades:
        especialidades += item+', '
    member.especialidades_str = especialidades.strip().strip(',')
    document['data-specialization'].text = member.especialidades_str
    
    def editCurriculum(ev):
        jQuery('#data-curriculum').fadeOut(jQuery('#profile-input-curriculum').fadeIn)
        jQuery('#profile-input-curriculum').val(member.curriculum)
        jQuery('#edit-curriculum').attr('src', '/static/image/complete_icon.svg')
        jQuery('#edit-curriculum').css('transform', 'scale(0.5')
        jQuery('.curriculum-container').css('height', '18vh')
        
        def completeCurriculumEdition(ev):
            if not member.curriculum == jQuery('#profile-input-curriculum').val():
                member.curriculum = jQuery('#profile-input-curriculum').val()
                _ajax('/update_profile/', print, method='POST', data=vars(member))
            jQuery('#data-curriculum').text(member.curriculum)
            jQuery('#profile-input-curriculum').fadeOut(jQuery('#data-curriculum').fadeIn)
            jQuery('#edit-curriculum').attr('src', '/static/image/edit.svg')
            jQuery('.curriculum-container').css('height', '15vh')
            jQuery('#edit-curriculum').css('transform', '')
            jQuery('#edit-curriculum').off('click')
            jQuery('#edit-curriculum').on('click', editCurriculum)
        jQuery('#edit-curriculum').off('click')
        jQuery('#edit-curriculum').on('click', completeCurriculumEdition)

    jQuery('#edit-curriculum').on('click', editCurriculum)

def loadSafety():
    def clearInputs():
        document['input-current-password'].value = ''
        document['input-new-password'].value = ''
        document['input-new-password-confirmation'].value = ''
        document['input-current-email'].value = ''
        document['input-new-email'].value = ''
        document['input-new-email-confirmation'].value = ''

    def successSafetyPopup(req):
        response = eval(req.text)
        safetyPopup(response[0], response[1])

    def safetyPopup(h1, p):
        POPUP.fadeToggle()
        toggleContainer(mode='blur')
        POPUP.find('h1').text(h1)
        POPUP.find('p').text(p)

    @bind('#change-password-button', 'click')
    def change_password_button(ev):
        current = document['input-current-password'].value
        new = document['input-new-password'].value
        new_confirmation = document['input-new-password-confirmation'].value

        if current and new and new_confirmation:
            if current == member.password:
                if new == new_confirmation:
                    _ajax('/change_password/', successSafetyPopup, 'POST',
                          data={'id': member.id, 'new_password': new})
                else:
                    safetyPopup(
                        'ERRO', 'Nova senha não confere com a confirmação')
            else:
                safetyPopup('ERRO', 'Senha atual inválida')

            timer.set_timeout(clearInputs, 500)

    @bind('#change-email-button', 'click')
    def change_email_button(ev):
        current = document['input-current-email'].value
        new = document['input-new-email'].value
        new_confirmation = document['input-new-email-confirmation'].value

        if current and new and new_confirmation:
            if current == member.email:
                if new == new_confirmation:
                    _ajax('/change_email/', successSafetyPopup, 'POST',
                          data={'id': member.id, 'new_email': new})
                else:
                    safetyPopup(
                        'ERRO', 'Novo e-mail não confere com a confirmação')
            else:
                safetyPopup('ERRO', 'e-mail atual inválido')

            timer.set_timeout(clearInputs, 500)


def loadRestrict(member):
    jQuery('#videos-container').hide()

    for element in document.select('.restrict-toolbar > h1'):
        tool = RestrictTool(element, element.attrs['name'][:-5])


def loadRequests(req):
    data = eval(req.text)

    # populate select list with options from database
    for item in data:
        option = f'<option value="{item[0]}">{item[1]}</option>'
        jQuery('#solicitacao').append(option)

    # populating request history
    def populateRequestHistory():
        count = 1
        for solicitacao in member.solicitacoes:
            row = f'<tr id="request-{solicitacao[0]}"><td>{solicitacao[6]}</td><td>{solicitacao[2]}</td><td class="request-situation">{solicitacao[3]}</td><td>{solicitacao[4]}</td></tr>'

            jQuery('#requests-history').append(row)

            if solicitacao[5]:
                jQuery(
                    f'#request-{solicitacao[0]}').append(f'<td><a download="{solicitacao[6]}.{solicitacao[5].split(".")[1]}" href="/static/documents/{member.id}/{solicitacao[5]}" title="Download"><img src="/static/image/download_icon.svg"></img></a></td>')
            else:
                jQuery(f'#request-{solicitacao[0]}').append(
                    f'<td><img id="cancel-request-{solicitacao[0]}" class="cancel-request" src="/static/image/x_icon.svg"></img></td>')

            count += 1
            if count > 5:
                break

        @bind('.cancel-request', 'click')
        def cancelRequestButton(ev):
            id = ev.target.attrs['id'].split('-')[2]
            print(f'clicked {id}')

            def cancelRequest(req):
                data = eval(req.text)
                print(f'response: {data}')
                toggleContainer('blur')
                POPUP.fadeToggle()
                POPUP.find('h1').text(data[0])
                POPUP.find('p').text(data[1])
                if data[0] == 'Sucesso':
                    jQuery(
                        f'#request-{id} > .request-situation').text('Encerrado')

            _ajax('/cancel_request/', cancelRequest,
                  method='POST', data={'id': id})

    populateRequestHistory()

    # hiding elements
    jQuery('.new-request-container').hide()
    jQuery('.new-request-toggles').hide()

    # binding buttons
    @bind('#visualization-button', 'click')
    def renderRequestsPage(ev):
        jQuery(
            '.new-request-container').fadeToggle(jQuery('.visualization-container').fadeToggle)

    @bind('#new-request-button', 'click')
    def renderNewRequestPage(ev):
        jQuery(
            '.visualization-container').fadeToggle(jQuery('.new-request-container').fadeToggle)

    # NOVA SOLICITAÇÃO
    @bind('#submit-request-button', 'click')
    def submitRequest(ev):
        def addRequestToTable(solicitacao, today, protocolo):
            new = [len(member.solicitacoes), member.id,
                   solicitacao, 'Em Andamento', today, '', protocolo]
            member.solicitacoes.insert(0, new)

            jQuery('#requests-history tr:not(.table-header > tr)').remove()
            populateRequestHistory()
            jQuery('.requests-history tr:nth-child(odd)').css('background-color',
                                                              'white')
            jQuery('.requests-history tr:nth-child(even)').css('background-color',
                                                               'var(--table-row-background)')

        def newRequest(req):
            data = eval(req.text)
            h1 = data[0]
            p = data[1]
            POPUP.find('h1').text(h1)
            POPUP.find('p').text(p)
            if not data[0] == 'error':
                addRequestToTable(data[2], data[3], data[4])
            POPUP.find('button').fadeToggle()

        data = {
            'id': member.id,
            'request': document['solicitacao'].value
        }

        toggleContainer(mode='blur')
        POPUP.fadeToggle()
        POPUP.find('h1').text('Carregando')
        POPUP.find('p').text('Gerando solicitação')
        POPUP.find('button').hide()

        _ajax('/new_request/', newRequest, method='POST', data=data)
        jQuery('#solicitacao').val('')
        jQuery('.new-request-toggles').hide()
        jQuery('.new-request-container').hide()
        jQuery('.visualization-container').fadeToggle()

    # rendering description when changing the select list

    @bind('#solicitacao', 'change')
    def getRequestValue(ev):
        document['solicitacao-desc'].text = data[int(ev.target.value)][2]
        jQuery('.new-request-toggles').fadeIn()

def loadMember():
    loadProfile()
    loadSafety()
    loadActivePlan(member)
    loadRestrict(member)
    _ajax('/get_videos/', videosList)
    _ajax('/get_blog/', restrictContentList)
    _ajax('/available_requests/', loadRequests)

def preLoad(req):
    global member

    data = eval(req.text)
    member = Member(data)

    if member.type:
        loadMember()
    initialRender()


def _ajax(url, onComplete, method='GET', data={}):
    req = ajax.Ajax()
    req.bind('complete', onComplete)
    req.open(method, url, True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send(data)


@bind('#camera-icon-container', 'click')
def uploadPicture(ev):
    alert('caixa de diálogo pra upload de foto')


_ajax('/get_member/', preLoad)
