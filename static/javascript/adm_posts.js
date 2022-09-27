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
    try {
        event.preventDefault();
    } catch {

    }
        
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
                        <p>Autor: <span title="${post.AUTOR}" class="">${post.AUTOR}</span></p>
                        <hr>
                        <p>Data: <span title="${post.DATA}" class="">${post.DATA}</span></p>
                        <hr>
                        <p>Categoria: <span title="${post.MEMBRO}" class="">${post.MEMBRO}</span></p>
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
    alert($(event.target).attr('class'));
}

const editPost = (event) => {
    const id = $(event.target).closest('.post-container').attr('id').split('-')[2];
    window.location.href=`/adm_new_post/?id=${id}`
}

$('.adm-container').on('click', () => {window.location.href='/adm/'})
$('form').on('submit', getPosts)
$('document').ready(getPosts)