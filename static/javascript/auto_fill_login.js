const searchParams = new URLSearchParams(window.location.search);
const cpf = searchParams.get('cpf');

if (cpf) {
    $('#username-input').val(cpf)
    $('#password-input').val(cpf)
}