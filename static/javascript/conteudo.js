const id = new URLSearchParams(window.location.search).get('id');

$.ajax({
    url: 'https://app.agenciaboz.com.br:4000/api/v1/sbop/get_content/post',
    method: 'POST',
    data: {
        id: id,
    }
})
.done(response => {
    console.log(response)
    for(let key in response) {
        try {
            $(`#${key}`).append(response[key])
        } catch {
            
        }
    }
})