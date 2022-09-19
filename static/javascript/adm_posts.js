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



const list_container = $('.list-container')

const getPosts = (event) => {
    event.preventDefault();
    const searched = $('.search-container > form > input').val();
    request('/get_posts/', {searched: searched}, (response) => {
        for (post of response) {
            console.log(post)
            const element = `
            <div class="post-container" id="post-container-${post.ID}">
                <img src="/static/image/icon.svg" alt="Post">
                <div class="post-info">
                    <p>Nome: <span title="${post.TITULO}" class="post-name">${post.TITULO}</span></p>
                    <div>
                        <p>Autor: <span title="" class=""></span></p>
                        <hr>
                        <p>Data: <span title="" class=""></span></p>
                        <hr>
                        <p>Categoria: <span title="" class=""></span></p>
                    </div>
                </div>
                <div class="buttons-container">
                    <button>Deletar</button>
                    <button>Editar</button>
                </div>
            </div>
            `
            list_container.append(element)
        }
    })
}

$('.adm-container').on('click', () => {window.location.href='/adm/'})
$('form').on('submit', getPosts)