const posts_container = $('#publicacoes-container');
const videos_container = $('#videos-container');

const get_member = setInterval(() => {
    if (membro.exists) {
        clearInterval(get_member);

        getContentList(membro);
    }
}, 100);

const getContentList = (membro) => {
    $.ajax({
        method: 'POST',
        url: '/get_member_posts/',
        contentType: 'application/json',
        data: JSON.stringify({ assinatura: membro.assinatura })
    })
        .done((response) => {
            const posts = JSON.parse(response);

            for (const post of posts) {
                if (!post.video) {
                    console.log(post);
                    const element = `
                <div class="restrict-content-wrapper">
                    <img class="restrict-media" src="/static/conteudos/${post.id}" alt="Teste">
                    <div class="restrict-content-data">
                        <h1 class="content-title">${post.titulo}</h1>
                        <p class="restrict-content-author">${post.autor} - ${post.data}</p>
                        <div class="content-box">
                            <p>${post.resumo}</p>
                            <br>
                            <p>${post.conteudo}</p>
                        </div>
                    </div>
                </div>
                <hr>
                `
                    posts_container.append(element);
                } else {
                    console.log(post);
                    const element = `
                <div class="restrict-content-wrapper">
                    <video class="restrict-media" controls>
                        <source src="/static/conteudos/${post.id}" type="video/mp4">
                    </video>
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
                    videos_container.append(element);
                }
            }
        });
}
