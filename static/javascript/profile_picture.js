const profile_picture = $('#profile-picture');

const get_member3 = setInterval(() => {
    if (membro.exists) {
        clearInterval(get_member3);

        loadProfilePicture(membro);
    }
}, 100);

const loadProfilePicture = (membro) => {
    profile_picture.attr('src', `/static/profile_pictures/${membro.id}`);
    
    setTimeout(() => $('#loading-screen').fadeToggle('slow'), 300);

    profile_picture.on('error', () => {
        console.log('foto de perfil não encontrada');
        profile_picture.attr('src', '/static/image/doctor_icon.svg');

        // profile_picture.on('error', null);
    });
};