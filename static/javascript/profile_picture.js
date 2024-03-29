const profile_picture = $('#profile-picture');
const input = $('#upload-pfp');

const get_member3 = setInterval(() => {
    if (membro.exists) {
        clearInterval(get_member3);

        loadProfilePicture(membro);
    }
}, 100);

const loadProfilePicture = (membro) => {
    profile_picture.attr('src', `/static/profile_pictures/${membro.id}`);

    setTimeout(() => {
        $('.body-container').show()
        $('#loading-screen').fadeToggle('slow')

        if (membro.pago) {
            $('#profile-picture').addClass('pfp-pago')
        }
    }, 300);

    profile_picture.on('error', () => {
        console.log('foto de perfil não encontrada');
        profile_picture.attr('src', '/static/image/doctor_icon.svg');

        // profile_picture.on('error', null);

    });
};

const sendPicture = (membro) => {
}

input.on('change', (event) => {
    form_data.append('file', input[0].files[0]);
    const data = {
        membro: membro,
    }


    form_data.append('data', JSON.stringify(data));
    console.log(data);
    $.ajax({
        type: 'POST',
        url: '/change_profile_picture/',
        data: form_data,
        processData: false,
        contentType: false
    }).done((response) => {
        res = JSON.parse(response)
        if (res.success) {
            profile_picture.removeAttr("src").attr('src', `/static/profile_pictures/${membro.id}?t=${new Date().getTime()}`);
        } else {
            alert(`erro ao atualizar a foto de perfil: ${res.error}`)
        }
    });
});