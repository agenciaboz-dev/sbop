$('form').on('submit', (event) => {
    event.preventDefault();
    if ($('#senha').val() === $('#confirmar-senha').val()) {
        const data = {
            id: $('input[type="hidden"]').val(),
            senha: $('#senha').val(),
        };

        const url = '/recover/'
    
        const options = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        };
        
        fetch(url, options)
        .then((response) => response.json())
        .then((data) => alert(JSON.stringify(data, null, 2)))
        .catch(err => console.error('error:' + err));

    } else {
        alert('Senhas não conferem');
    }
})