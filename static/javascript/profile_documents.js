const sendButton = $('#plans-save-button');
const form_data = new FormData();

const get_member2 = setInterval(() => {
    if (membro.exists) {
        clearInterval(get_member2);

        sendDocuments(membro);
    }
}, 100);

const sendDocuments = (membro) => {
    sendButton.on('click', (event) => {
        $('#documents-feedback').text('Enviando documentos...');
        form_data.append('file', $('#upload-file')[0].files[0]);
        const today = new Date();
        const data = {
            membro: membro,
        }


        form_data.append('data', JSON.stringify(data));
        console.log(data);
        $.ajax({
            type: 'POST',
            url: '/send_documents_titular/',
            data: form_data,
            processData: false,
            contentType: false
        }).done((response) => {
            $('#documents-feedback').text('Documentos enviados');
        });
    });
}