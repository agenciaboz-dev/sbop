let members = [];
let current_id;

const fromPython = (string) => {
    string = string.replaceAll(`"None"`, null);
    string = string.replaceAll(`"False"`, false);
    string = string.replaceAll(`"True"`, true);
    let data = JSON.parse(string)
    return data;
}

const loadList = () => {
    console.log('ready')
    $.ajax('/membros/').done((html) => {
        data = fromPython(html);
        members = data;

        buildList(members)
    });
}

const searchMember = (event) => {
    event.preventDefault();
    const searched = $('form > input').val();
    const request = $.ajax({
        url: '/membros/',
        method: 'POST',
        data: {
            search: 'name',
            value: searched,
            adm: true
        }
    });
    cleanList();
    $('.list-wrapper > h1').toggle();

    request.done((msg) => {
        data = fromPython(msg);
        $('#searched-text').text(searched);
        $('.list-wrapper > h1').toggle();
        data.shift();
        buildList(data);
    })
}

const cleanList = () => {
    $('.list-container > *').remove();
}

const buildList = (list) => {
    const container = $('.list-container');
    members = [];
    for (let member of list) {
        members.push(member)
        const member_container = `
            <div class="member-container" id="member-container-${member.id}">
                <img src="/static/image/doctor_icon.svg" alt="Doctor">
                <div class="member-info">
                    <p>Nome: <span title="${member.name}" class="member-name">${member.name}</span></p>
                    <div>
                        <p>CRM: <span title="${member.crm}" class="member-crm">${member.crm}</span></p>
                        <hr>
                        <p>CPF: <span title="${member.cpf}" class="member-cpf">${member.cpf}</span></p>
                    </div>
                </div>
                <hr>
                <div class="member-type-container">
                    <div class="member-type${member.member == 'Aspirante' ? ' active-type' : ''} Aspirante">Aspirante</div>
                    <div class="member-type${member.member == 'Associado' ? ' active-type' : ''} Associado">Associado</div>
                    <div class="member-type${member.member == 'Titular' ? ' active-type' : ''} Titular">Titular</div>
                </div>
                <img src="/static/image/${member.pago ? 'complete_icon.svg' : 'exclamacao2.svg'}" alt="Ícone">
            </div>
        `;
        container.append(member_container)
    }
    $('.member-container').on('click', onclickMember)
    $('.member-type').on('click', onClickMemberType)
}

const buildProfile = (member) => {
    current_id = member.id;
    $('#name-input').val(member.name);
    $('#user-input').val(member.user);
    $('#cpf-input').val(member.cpf);
    $('#password-input').val(member.password);
    $('#uf-input').val(member.uf);
    $('#cep-input').val(member.cep);
    $('#telefone-input').val(member.telefone);
    $('#celular-input').val(member.celular);
    $('#endereco-input').val(member.endereco);
    $('#numero-input').val(member.numero);
    $('#complemento-input').val(member.complemento);
    $('#bairro-input').val(member.bairro);
    $('#cidade-input').val(member.cidade);
    $('#pais-input').val(member.pais);
    $('#crm-input').val(member.crm);
    $('#curriculum-input').val(member.curriculum);
    $('#pessoa-input').val(member.pessoa);
    $('#temporario-input').val(member.temporario);
    $('#primeiro_acesso-input').val(member.primeiro_acesso);
    $('#especialidades-input').val(member.especialidades);
    $('#pago-input').val(member.pago);
}

const onclickMember = (event) => {
    $('.member-container-active').removeClass('member-container-active');

    const container = $(event.target).closest('.member-container');
    const id = container.attr('id').split('-')[2]

    container.addClass('member-container-active');
    const member = members.find(item => item.id == id)
    console.log(member)
    buildProfile(member)

}

const onClickSave = (event) => {
    const id = current_id;
    const inputs = $('.profile-data-field input');
    let member = {id: id}
    for (element of inputs) {
        const key = $(element).attr('id').split('-')[0]
        member[key] = $(element).val()
    }
    console.log(member)
    
    const request = $.ajax({
        url: '/edit_member/',
        method: 'POST',
        data: {
            search: 'name',
            nome: 'bosta'
        }
    });

    request.done((data) => {
        console.log(data)
    })
}

const onClickMemberType = (event) => {
    const container = $(event.target).closest('.member-container');
    const plan = $(event.target).text();
    const id = container.attr('id').split('-')[2]

    const member_type_container = $(event.target).closest('.member-type-container');
    const current_plan_container = member_type_container.children('.active-type');

    const request = $.ajax({
        url: '/change_plan/',
        method: 'POST',
        data: {
            id: id,
            plan: plan,
            adm: true
        }
    });

    member_type_container.addClass('deactivated');
    current_plan_container.removeClass('active-type');
    request.done((msg) => {
        if (msg == 'True') {
            $(event.target).closest(`.${plan}`).addClass('active-type');
        } else {
            current_plan_container.addClass('active-type');
        }
        member_type_container.removeClass('deactivated');
    })
}

$('form').on('submit', searchMember)
$('#profile-save-button').on('click', onClickSave)
$('document').ready(loadList)
