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

// Listen for messages from the parent document
window.addEventListener('message', event => {
    // Check the origin of the message to prevent unauthorized access
    // if (event.origin !== 'https://your-react-app.com') return;
  
    // Handle the message
    const {type, user, password} = event.data;
    if (type === 'login') {
        $('#username-input').val(user)
        $('#password-input').val(password)
        $('#login-form > button').trigger('click')
        
        event.source.postMessage('Message received!', event.origin)
    }
  });
  