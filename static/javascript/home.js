$('.recover-password').on('click', (event) => {
    $('#feedback').text('')
    $('.popup').fadeIn();
})

$('#x-button').on('click', (event) => {
    $('.popup').fadeOut();
})

$('#recover-form').on('submit', (event) => {
    const data = {user: $('#recover-input').val()};
    const url = '/recuperar/'
    event.preventDefault();

    const options = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    };
    
    fetch(url, options)
    .then((response) => response.json())
    .then((data) => {
        $('#feedback').text(data.msg)
    })
    .catch(err => console.error('error:' + err));
})