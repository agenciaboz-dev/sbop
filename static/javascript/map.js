const map = $('.map-container svg');
const width = $(window).width();

const mapScale = (width) => {
    map.css('transform', `scale(${width/1100})`);
    
    if (width < 640) {
        map.css('transform', `scale(${width/600})`);
        // $('#member-tooltip').css('width', `${$('#result').width()}`);
    }
}

$('document').ready(() => {
    mapScale(width)
})

$('#searched-hidden').on('change', () => {
    if ($('#searched-hidden').val()) {
        $('.doctor-icon').each((i, obj) => {
            const id = $(obj).attr('id').split('-')[2]
            $(obj).on('error', () => {
                $(obj).attr('src', '/static/image/doctor_icon.svg')
            })
            $(obj).attr('src', `/static/profile_pictures/${id}`)
        })
        $('#searched-hidden').val(false)
    }
})

$(window).on('resize', () => {
    mapScale($(window).width())
})