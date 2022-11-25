const request = (url, data, done) => {
    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    };

    fetch(url, options)
        .then((response) => response.json())
        .then((data) => done(data))
        .catch(err => console.error('error:' + err));
}



const list_container = $('.list-container')

const getPosts = (event) => {
    try {
        event.preventDefault();
    } catch {

    }

    $('.list-container > *').remove();
    const searched = $('.search-container > form > input').val();
    
    request('/get_posts/', { searched: searched }, (response) => {
        console.log(response);
        for (post of response) {
            console.log(post)
            const element = `
            <div class="post-container" id="post-container-${post.id}">
                <img src="/static/image/icon.svg" alt="Post">
                <div class="post-info">
                    <p>Nome: <span title="${post.titulo}" class="post-name">${post.titulo}</span></p>
                    <div>
                        <p>Autor: <span title="${post.autor}" class="">${post.autor}</span></p>
                        <hr>
                        <p>Data: <span title="${post.data}" class="">${post.data}</span></p>
                        <hr>
                        <p>Categoria: <span title="${post.categoria}" class="">${post.categoria}</span></p>
                    </div>
                </div>
                <div class="buttons-container">
                    <button class='delete-button'>Deletar</button>
                    <button class='edit-button'>Editar</button>
                </div>
            </div>
            `
            list_container.append(element);
        }
        $('.delete-button').on('click', deletePost);
        $('.edit-button').on('click', editPost);
    })
}


const deletePost = (event) => {
    const id = $(event.target).closest('.post-container').attr('id').split('-')[2];
    // alert($(event.target).attr('class'));
    if (confirm(`Tem certeza que deseja deletar a publicação?`)) {
        request('/delete_post/', {id}, (response) => {
            setTimeout(() => $(event.target).closest('.post-container').hide(), 500)
        })
    }
}

const editPost = (event) => {
    const id = $(event.target).closest('.post-container').attr('id').split('-')[2];
    window.location.href = `/adm_new_post/?id=${id}`
}

$('#sair-button').on('click', () => { window.location.href = '/logout/' })
$('#meu-perfil-button').on('click', () => { window.location.href = '/perfil/' })
$('#ir-para-adm-button').on('click', () => { window.location.href = '/adm/' })
$('#nova-postagem-button').on('click', () => { window.location.href = '/adm_new_post/' })
$('form').on('submit', getPosts)
$('document').ready(getPosts)