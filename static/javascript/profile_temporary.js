// stage 1 being handled on brython

const get_stage_2 = setInterval(() => {
    if (document.getElementById("stage-2-button")) {
        clearInterval(get_stage_2);

        $('#stage-2-button').on('click', () => {
            $('#temporary-container').fadeOut(() => {
                $('#plans-container').fadeIn()
            })
            
        })
    }
}, 100);

