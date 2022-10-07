$('form').on('submit', () => {
    if (!$('.person-type:checked').length) {
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
        pessoa: $('.person-type:checked').val(),
        temporario: true,
        primeiro_acesso: false,
        cpf: $('#cpf').val(),
        especialidades: especialidades,
        pago: false,
        adm: false,
        lat: 0,
        lng: 0
    }

    alert(JSON.stringify(data, null, 2));
})