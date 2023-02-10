const searchParams = new URLSearchParams(window.location.search);
const id = searchParams.get('id');
const form_data = new FormData();
let membro = {};
let file = null;

const editor = new FroalaEditor('#froala', {
    language: 'pt_br',
    charCounterCount: false,
    toolbarSticky: true,
});

const request = (url, data, done, method = 'POST', content_type = { 'Content-Type': 'application/json' }) => {
    const options = {
        method: method,
    };

    if (content_type) {
        options.headers = content_type;
    }

    if (method == 'POST') {
        options.body = JSON.stringify(data);
    }
    console.log(options);
    fetch(url, options)
        .then((response) => response.json())
        .then((data) => done(data))
        .catch(err => console.error('error:' + err));
}

$('document').ready(() => {

    $.ajax({
        method: 'GET',
        url: 'https://app.agenciaboz.com.br:4000/api/v1/sbop/get_category',
    })
    .done(response => {
        for (const categoria of response) {
            const element = `<option value="${categoria.nome.toLowerCase()}" selected>${categoria.nome}</option>`
            $('#category-input').append(element)
        }
    })

    if (!id) {

        request('/get_member/', {}, (response) => {
            membro = response;

            for (let item in membro) {
                if (typeof membro[item] == 'string') {
                    membro[item] = membro[item].replaceAll('False', false);
                    membro[item] = membro[item].replaceAll('True', true);
                    membro[item] = membro[item].replaceAll('None', null);
                    try {
                        membro[item] = JSON.parse(membro[item]);
                    } catch { }
                }
            }
            $('#author').text(`Autor: ${membro.name}`);
            console.log(membro);
        }, method = 'GET');

    } else {
        $('#publish-button').text('Atualizar')
        request('/get_post/', { id: id }, (response) => {
            console.log(response[0]);
            const post = response[0];

            $('#title-area').val(post.titulo);
            $('#content-area').val(editor.html.set(post.conteudo));
            $('#membership-input').val(post.assinatura);
            $('#category-input').val(post.categoria);
            $('#summary-area').val(post.resumo);
            $('#author').text(`Autor: ${post.autor}`);

            if (post.video) {
                $('#video-input').prop('checked', true);
            } else {
                $('#publish-input').prop('checked', true);
            }
        })
    }
})

$('#publish-button').on('click', (event) => {
    if (id) {
        const data = {
            id: id,
            titulo: $('#title-area').val(),
            conteudo: editor.html.get(),
            assinatura: $('#membership-input').val(),
            resumo: $('#summary-area').val(),
            categoria: $('#category-input').val().toLowerCase()
        }

        if (file) {
            form_data.append('file', $('#upload-file')[0].files[0]);


            form_data.append('data', JSON.stringify(data));
            $.ajax({
                type: 'POST',
                url: '/edit_post/',
                data: form_data,
                processData: false,
                contentType: false
            }).done((response) => {
                window.location.href = '/adm_posts/'
            });

        } else {
            console.log(data)
            request('/edit_post/', data, (response) => {
                console.log(response);
                window.location.href = '/adm_posts/'
            });
        }

    } else {
        if (!$('input[name="post-input"]:checked').length) {
            alert('Escolha entre publicação ou vídeo');
            return false;
        }

        if (!file) {
            alert('Envie uma imagem');
            return false;
        }

        if (!$('#summary-area').val()) {
            alert('Preencha o resumo');
            return false;
        }

        if (!$('#title-area').val()) {
            alert('Preencha o título');
            return false;
        }

        form_data.append('file', $('#upload-file')[0].files[0]);
        const today = new Date();
        const data = {
            video: $('input[name="post-input"]:checked').attr('id').split('-')[0] == 'video' ? true : false,
            assinatura: $('#membership-input').val(),
            resumo: $('#summary-area').val(),
            titulo: $('#title-area').val(),
            conteudo: editor.html.get(),
            categoria: $('#category-input').val().toLowerCase(),
            autor: membro.name,
            data: today.toLocaleDateString(),
        }


        form_data.append('data', JSON.stringify(data));
        console.log(data);
        $.ajax({
            type: 'POST',
            url: '/new_post/',
            data: form_data,
            processData: false,
            contentType: false
        }).done((response) => {
            window.location.href = '/adm_posts/'
        });
    }
})

$('#cancelar-button').on('click', () => {
    window.location.href = '/adm_posts/';
})

$('#upload-file').on('change', () => {
    file = true;
})