let members;
const loadList = () => {
    console.log('ready')
    $.ajax('/membros/').done((html) => {
        data = String.raw`${html}`;
        data = data.replaceAll(`None`, `null`);
        data = JSON.parse(data);
        members = data;

        buildList(members)
    });
}

const searchMember = (event) => {
    event.preventDefault();
    const searched = $('form > input').val()
    alert(searched)
}

const cleanList = () => {
    $('.list-container > *').remove();
}

const buildList = (list) => {
    const container = $('.list-container');
    for (let member of list) {
        member.pago = member.pago == 'False' ? false : true;
        const member_container = `
            <div class="member-container" id="${member.id}">
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
                    <div class="member-type${member.member == 'Aspirante' ? ' active-type' : ''}">Aspirante</div>
                    <div class="member-type${member.member == 'Associado' ? ' active-type' : ''}">Associado</div>
                    <div class="member-type${member.member == 'Titular' ? ' active-type' : ''}">Titular</div>
                </div>
                <img src="/static/image/${member.pago ? 'complete_icon.svg' : 'exclamacao.svg'}" alt="Ícone">
            </div>
        `;
        container.append(member_container)
    }
}

const renderProfile = (member) => {
    const container = $('.profile-data-field')
    const editaveis = [
        'name',
        'cpf', 
        'uf', 
        'cep', 
        'email', 
        'telefone', 
        'celular', 
        'endereco', 
        'numero', 
        'complemento', 
        'bairro', 
        'cidade', 
        'pais', 
        'crm'
    ];

    for (key of editaveis) {
        const input_container = `
            <div class="input-field">
                <label for="${key}-input">${key}</label>
                <input id="${key}-input" type="text" placeholder="${key}">
            </div>
        `;
        container.append(input_container)
    }

}

$('form').on('submit', searchMember)
$('document').ready(loadList)
$('document').ready(renderProfile)