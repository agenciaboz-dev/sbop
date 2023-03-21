const searchParams = new URLSearchParams(window.location.search);
const adm_id = searchParams.get('id');

let members = [];
let current_id;
const profile_picture = $('#profile-picture')

const fromPython = (string) => {
    string = string.replaceAll(`"None"`, null);
    string = string.replaceAll(`"False"`, false);
    string = string.replaceAll(`"True"`, true);
    let data = JSON.parse(string)
    return data;
}

const deleteMember = (id) => {
    $.ajax({
        method: "POST",
        url: "https://app.agenciaboz.com.br:4000/api/v1/sbop/delete_member", // nodejs
        data: { id, adm_id }
    }).done(response => {
        searchMember()
        console.log(response)
    })
}

const loadProfilePicture = (membro) => {
    profile_picture.attr('src', `/static/profile_pictures/${membro.id}`);

    setTimeout(() => $('#loading-screen').fadeToggle('slow'), 300);

    profile_picture.on('error', () => {
        console.log('foto de perfil não encontrada');
        profile_picture.attr('src', '/static/image/doctor_icon.svg');

    });
};

const getEspecialidades = () => {
    const container = $('.especialidades-inputs-container')
    $.get('/especialidades', (response) => {
        const especialidades = JSON.parse(response);
        for (let especialidade of especialidades) {
            element = `
            <div>
                <input type="checkbox" value="${especialidade.nome}" class="checkbox"
                    id="member-input-${especialidade.nome.toLowerCase().split(' ')[0]}" name="especialidades-input">
                <label for="member-input-${especialidade.nome.toLowerCase().split(' ')[0]}">${especialidade.nome}</label>
            </div>
            `
            container.append(element);
        }
    })

}

const loadList = () => {
    console.log('ready')
    $.ajax('/membros/').done((html) => {
        data = fromPython(html);
        members = data;
        console.log(members)

        buildList(members);
        getEspecialidades();
    });
}

const searchMember = (event) => {
    if (event) event.preventDefault();
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

    // mobile
    if ($(window).width() < $(window).height()) {
        $('.member-container').on('click', () => {
            profile.show();
            $('.list-wrapper').hide();
        })
    }
}

const buildProfile = (member) => {
    current_id = member.id;
    $('#name-input').val(member.name);
    $('#user-input').val(member.user);
    $('#cpf-input').val(member.cpf);
    $('#email-input').val(member.email);
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

    if (member.pessoa == 1) {
        $('#pessoa-fisica-input').prop("checked", true);
    } else {
        $('#pessoa-juridica-input').prop("checked", true);
    }

    const especialidades = member.especialidades.split(',');

    $('input[name="especialidades-input"]').prop('checked', false);
    for (let especialidade of especialidades) {
        $(`input[value="${especialidade}"]`).prop('checked', true);
    }

    if (member.temporario === true || member.temporario === "true") {
        $('#temporario-input').prop("checked", true);
    } else {
        $('#temporario-input').prop("checked", false);

    }

    if (member.primeiro_acesso) {
        $('#primeiro_acesso-input').prop("checked", true);
    } else {
        $('#primeiro_acesso-input').prop("checked", false);

    }

    if (member.pago) {
        $('#pago-input').prop("checked", true);
    } else {
        $('#pago-input').prop("checked", false);

    }

    if (!member.member) {
        $('#pago-input').prop("disabled", true)
    } else {
        $('#pago-input').prop("disabled", false)
    }

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
    let member = { id: id, adm_panel: true }
    for (element of inputs) {
        const key = $(element).attr('id').split('-')[0]
        member[key] = $(element).val()
    }
    member.uf = $('#uf-input').val()
    member.especialidades = ''

    for (let element of $('input[name="especialidades-input"]:checked')) {
        member.especialidades += `${$(element).val()},`
    }

    member.temporario = Boolean($('#temporario-input:checked')[0]);
    member.primeiro_acesso = Boolean($('#primeiro_acesso-input:checked')[0]);
    member.pago = Boolean($('#pago-input:checked')[0]);
    console.log(member)

    const requisicaoUngida = () => {
        const url = '/edit_member/';

        const options = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(member)
        };

        fetch(url, options)
            .then(res => res.json())
            .then(response => {
                console.log(response)
                if (response.error) alert(response.error)
            })
            .catch(err => console.error('error:' + err));
    }

    if (confirm(`Tem certeza que deseja atualizar os dados do usuário ${member.user}?`)) {
        requisicaoUngida()
        setTimeout(() => searchMember(), 1000)

        // mobile
        if ($(window).width() < $(window).height()) {
            profile.hide();
            $('.list-wrapper').show();
    }
    }
}

const onClickCancel = (event) => {
    const id = current_id;
    const member = members.find(item => item.id == id)
    buildProfile(member)
}

const onClickMemberType = (event) => {
    const container = $(event.target).closest('.member-container');
    const plan = $(event.target).text();
    const id = container.attr('id').split('-')[2]

    const member_type_container = $(event.target).closest('.member-type-container');
    const current_plan_container = member_type_container.children('.active-type');

    if (confirm(`Tem certeza que deseja alterar o tipo do usuário para ${plan}?`)) {
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

}

$('#profile-delete-button').on('click', () => {
    const id = current_id;
    const member = members.find(item => item.id == id)
    if (confirm(`Você tem certeza de que gostaria de deletar ${member.name}? As informações desse usuário não poderão ser recuperadas e essa ação ficará registrada em nosso histórico.`)) {
        deleteMember(id)
    }
})
$('#sair-button').on('click', () => { window.location.href = '/logout/' })
$('#meu-perfil-button').on('click', () => { window.location.href = '/perfil/' })
$('#ir-para-postagens-button').on('click', () => { window.location.href = '/adm_posts/' })
$('form').on('submit', searchMember)
$('#profile-save-button').on('click', onClickSave)
$('#profile-reset-button').on('click', onClickCancel)
$('document').ready(loadList)

/* MOBILE STYLING */
const profile = $('.profile-container');
if ($(window).width() < $(window).height()) {
    profile.hide();
    profile.css('position', 'absolute');

    $('#profile-reset-button').on('click', () => {
        profile.hide();
        $('.list-wrapper').show();
    })

}