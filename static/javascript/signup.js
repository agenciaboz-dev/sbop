$('form').on('submit', (event) => {
    event.preventDefault();
    if (!$('input[name="pessoa"]:checked').length) {
        alert('selecione um tipo de pessoa');
        return false
    }

    especialidades = ''

    for (let element of $('.skill-slot:checked')) {
        especialidades += `${$(element).val()},`
    }

    const data = {
        user: $('#usuario').val(),
        senha: $('#senha').val(),
        nome: $('#nome').val(),
        uf: $('#estado').val(),
        cep: $('#cep').val(),
        email: $('#email').val(),
        telefone: $('#telefone').val(),
        celular: $('#celular').val(),
        endereco: $('#endereco').val(),
        numero: $('#numero').val(),
        complemento: $('#complemento').val(),
        bairro: $('#bairro').val(),
        cidade: $('#cidade').val(),
        pais: $('#pais').val(),
        crm: $('#crm').val(),
        curriculum: $('#curriculum').val(),
        pessoa: $('input[name="pessoa"]:checked').val(),
        temporario: 'False',
        primeiro_acesso: 'False',
        cpf: $('#cpf').val(),
        especialidades: especialidades,
        pago: 'False',
        adm: 'False',
        lat: 0,
        lng: 0
    }

    console.log(data)

    $.ajax({
        type: 'POST',
        url: '/cadastro/',
        data: JSON.stringify(data),
        processData: false,
        contentType: 'application/json'
    }).done((response) => {
        const res = JSON.parse(response);
        if (res.success) {
            window.location.href = '/home/';
        } else {
            $('#feedback').text(res.error);
        }
    });
})