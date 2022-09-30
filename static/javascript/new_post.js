const searchParams = new URLSearchParams(window.location.search);
const id = searchParams.get('id');
const form_data = new FormData();
let membro = {};

const request = (url, data, done, method='POST', content_type = {'Content-Type': 'application/json'}) => {
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
    $('#publish-input').prop('checked', true);

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
                        } catch {}
                    }
                }
                $('#author').text(`Autor: ${membro.name}`);
                console.log(membro);
        }, method='GET');
    } else {
        request('/get_post/', {id: id}, (response) => {
            console.log(response[0]);
            const post = response[0];
            
            $('#title-area').val(post.titulo);
            $('#content-area').val(post.conteudo);
            $('#category-input').val(post.categoria);
            $('#summary').val(post.resumo);
            $('#author').text(`Autor: ${post.autor}`);
        })
    }
})

$('#publish-button').on('click', (event) => {
    if (id) {
        request('/edit_post/', {
            id: id,
            titulo: $('#title-area').val(),
            conteudo: $('#content-area').val(),
            membro: $('#category-input').val(),
            resumo: $('#summary').val(),
        }, (response) => {
            console.log(response);
            alert(JSON.stringify(response, null, 2));
        });
    } else {
        form_data.append('file', $('#upload-file')[0].files[0]);
        const today = new Date();
        const data = {
            video: $('input[name="post-input"]:checked').attr('id').split('-')[0] == 'video' ? true : false,
            categoria: $('#category-input').val(),
            resumo: $('#summary').val(),
            titulo: $('#title-area').val(),
            conteudo: $('#content-area').val(),
            autor: membro.name,
            data: today.toLocaleDateString(),
            capa: form_data,
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
            alert(JSON.stringify(response, null, 2));
        });
    }
})

$('#cancelar-button').on('click', () => {
    window.location.href='/adm_posts/';
})