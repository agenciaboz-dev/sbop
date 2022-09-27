const searchParams = new URLSearchParams(window.location.search);
const id = searchParams.get('id');

const request = (url, data, done) => {
    const options = {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
    };

    fetch(url, options)
    .then((response) => response.json())
    .then((data) => done(data))
    .catch(err => console.error('error:' + err));
}

$('document').ready(() => {
    if (!id) {
        
        return false;
    }
    request('/get_post/', {id: id}, (response) => {
        console.log(response[0]);
        const post = response[0];
        
        $('#title-area').val(post.TITULO);
        $('#content-area').val(post.CONTEUDO);
        $('#category-input').val(post.MEMBRO);
        $('#summary').val(post.RESUMO);
        $('#author').text(`Autor: ${post.AUTOR}`);
    })
})

$('#publish-button')