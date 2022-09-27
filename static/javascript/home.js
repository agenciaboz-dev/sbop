$('.recover-password').on('click', (event) => {
    $('.popup').fadeToggle();
})

$('#recover-form').on('submit', (event) => {
    const data = {user: $('#recover-input').val()};
    const url = '/recuperar/'
    event.preventDefault();
    $('.popup').fadeToggle();

    const options = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    };
    
    fetch(url, options)
    .then((response) => response.json())
    .then((data) => alert(JSON.stringify(data, null, 2)))
    .catch(err => console.error('error:' + err));
})