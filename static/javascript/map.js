const map = $('.map-container svg');
const width = $(window).width();

$('document').ready(() => {
    map.css('transform', `scale(${width/1100})`);
    
    if (width < 640) {
        map.css('transform', `scale(${width/600})`);
        // $('#member-tooltip').css('width', `${$('#result').width()}`);
    }
})