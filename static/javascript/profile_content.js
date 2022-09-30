const posts_container = $('#publicacoes-container');

const get_member = setInterval(() => {
    if (membro.exists) {
        clearInterval(get_member);

        getContentList(membro);
    }
}, 100);

const getContentList = (membro) => {
    $.ajax({
        method: 'POST',
        url: '/get_member_posts',
        contentType: 'application/json',
        data: JSON.stringify({ assinatura: membro.assinatura })
    })
    .done((response) => {
        const posts = JSON.parse(response);
        
        for (const post of posts) {
            console.log(post);
            const element = `
            <div class="restrict-content-wrapper">
                <img class="restrict-media" src="/static/conteudos/${post.id}" alt="Teste">
                <div class="restrict-content-data">
                    <h1 class="content-title">${post.titulo}</h1>
                    <p class="restrict-content-author">${post.autor} - ${post.data}</p>
                    <p>${post.resumo}</p>
                    <br>
                    <p>${post.conteudo}</p>
                </div>
            </div>
            <hr>
            `
            posts_container.append(element)
        }
    });
}