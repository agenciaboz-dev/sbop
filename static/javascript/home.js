$('.recover-password').on('click', (event) => {
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
    .then((data) => (data) => {
        console.log(data);
        $('#feedback').text(data)
    })
    .catch(err => console.error('error:' + err));
})