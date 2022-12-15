const posts_container = $('#publicacoes-container');
const videos_container = $('#videos-container');

const get_member = setInterval(() => {
    if (membro.exists) {
        clearInterval(get_member);

        getContentList(membro);
    }
}, 100);

$('document').ready(() => {
    getCategoryList()
})

const getCategoryList = () => {
    $.ajax({
        method: 'GET',
        url: 'http://app.agenciaboz.com.br:4001/api/v1/sbop/get_category',
    })
        .done(response => {
            for (const categoria of response) {
                const element = `<h2 value="${categoria.nome.toLowerCase()}">${categoria.nome}</h2>`
                $('.category-select').append(element)
            }

            $($('.category-select').children()[0]).addClass('selected-category')

            $('.category-select').children().on('click', (event) => {
                $('.selected-category').removeClass('selected-category')
                $(event.target).addClass('selected-category')

                $('#publicacoes-container').children().remove()

                getContentList(membro)
            })
        })
}

const getContentList = (membro) => {
    $.ajax({
        method: 'POST',
        url: 'http://app.agenciaboz.com.br:4001/api/v1/sbop/get_content',
        contentType: 'application/json',
        data: JSON.stringify({ assinatura: membro.assinatura, categoria: $('.selected-category').attr('value') })
    })
        .done((response) => {
            const posts = response;

            for (const post of posts) {
                if (!post.video) {
                    console.log(post);
                    const element = `
                <section class="post-wrapper" post="${post.id}" style="display: contents;">
                    <div class="restrict-content-wrapper">
                        <img class="restrict-media view-post" src="/static/conteudos/${post.id}" onerror="if (this.src != '/static/image/default_content.webp') this.src = '/static/image/default_content.webp';" alt="SBOP">
                        <div class="restrict-content-data">
                            <h1 class="content-title view-post">${post.titulo}</h1>
                            <p class="restrict-content-author">${post.autor} - ${post.data}</p>
                            <div class="content-box">
                                <p>${post.resumo}</p>
                                <br>
                                <p>${post.conteudo}</p>
                            </div>
                        </div>
                    </div>
                    <h1 class="learn-more-button view-post">Saiba Mais</h1>
                </section>
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
            $('.view-post').on('click', (ev) => {
                const id = $(ev.target).closest('.post-wrapper').attr('post')
                window.open(`/conteudo/?id=${id}`, '_self').focus();
            })
        });
}


