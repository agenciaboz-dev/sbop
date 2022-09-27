const especialidades_button = $('#edit-skills')
const popup = $('#js-floating-popup')
let membro = {}

const request = (url, data, done) => {
    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    };

    fetch(url, options)
        .then((response) => response.json())
        .then((data) => done(data))
        .catch(err => console.error('error:' + err));
}


$('document').ready(() => {
    popup.hide();
    $.get('/especialidades/', (response) => {
        const especialidades = JSON.parse(response);

        popup.find('h1').text('Especialidades')
        popup.find('button').text('Confirmar')
        for (let especialidade of especialidades) {
            popup.find('>div').append(`
            <div>
                <input name="especialidades-data" type="checkbox" id="especialidades-data-${especialidade.nome.toLowerCase().split(' ')[0]}" value="${especialidade.nome}" />
                <label for="especialidades-data-${especialidade.nome.toLowerCase().split(' ')[0]}">${especialidade.nome}</label>
            </div>`)
        };

        popup.find('button').on('click', () => {

            popup.fadeToggle();
            let novas_especialidades = '';
            for (item of $('input[name="especialidades-data"]:checked')) {
                novas_especialidades += `${$(item).val()},`;
            }
            request('/trocar_especialidade/', {
                id: popup.attr('member-id'),
                especialidades: novas_especialidades,
            }, (response) => {
                let especialidades = '';
                for (let especialidade of response.especialidades.split(',')) {
                    especialidades += `${especialidade}, `
                }
                // especialidades[especialidades.length-1] = '';
                $('#data-specialization').text(especialidades);
            });
        });

        especialidades_button.on('click', (event) => {
            const antigas_especialidades = $('#data-specialization').text().replaceAll(', ', ',').split(',');
            console.log(antigas_especialidades);
            $('input[name="especialidades-data"]').prop('checked', false);
            for (especialidade of antigas_especialidades) {
                console.log(especialidade);
                $(`input[value="${especialidade}"]`).prop('checked', true);
            }

            popup.fadeToggle();
        });
    });

    $('.documents-container').hide();

})

const get_member = setInterval(() => {
    if (popup.attr('member-id')) {
        setTimeout(() => {
            
            request('/get_member_js/', {
                id: popup.attr('member-id'),
                test: 'test',
                
            }, (response) => {
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
                console.log(membro);
    
                if (membro.pago) {
                    $('#upgrade-plan-button').on('click', (event) => {
                        if ($('.active-plan').attr('id') == 'associado') {
                            $('.documents-container').fadeToggle();
                        }
                    });
                } else {
                    alert('seguir pro pagamento');
                }
            });
        }, 1000)
        clearInterval(get_member);
    }
}, 1000);