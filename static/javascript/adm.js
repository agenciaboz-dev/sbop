let members;

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
    for (let member of list) {
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

const onclickMember = (event) => {
    $('.member-container-active').removeClass('member-container-active');

    const container = $(event.target).closest('.member-container');
    container.addClass('member-container-active');
    
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
$('document').ready(loadList)