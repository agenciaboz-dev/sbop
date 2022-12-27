const mobile = $(window).width() < $(window).height();
const especialidades_button = $('#edit-skills')
const popup = $('#js-floating-popup')
var membro = {}

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
    $('.payment-container').hide();

})

const resetText = () => {
    $('#clipboard-button').text('Clique aqui para copiar a chave Pix')
}

// botão de copiar o qrcode
const copyToClipboard = (texto) => {
    $('#clipboard-button').on('click', () => {
        let $temp = $("<input>");
        $("body").append($temp);
        $temp.val(texto).select();
        document.execCommand("copy");
        $temp.remove();
        $('#clipboard-button').text('Chave PIX copiada')
        setTimeout(resetText, 1000)
    })
}

const tipoPagamento = (plano) => {
    console.log(plano)
    const plan_name = $('.payment-header > div > h1 > span')
    const plan_value = $('.payment-header > div > h2 > span')
    const plan_qrcode = $('.qr-container > img')

    const inicial = plano.slice(0, 1).toUpperCase()
    plan_name.text(inicial + plano.slice(1))

    if (plano == 'aspirante') {
        plan_value.text(200)
        plan_qrcode.attr('src', '/static/image/QR Code 200.svg')
        copyToClipboard('00020126920014BR.GOV.BCB.PIX0114650851360001970252Pagamento referente a anuidade como membro aspirante5204000053039865406200.005802BR5904SBOP6009SAO PAULO622605226efbqxL6fjSRPouvW6fhzT6304D7C9')
    }
    else if (plano == 'associado') {
        plan_value.text(400)
        plan_qrcode.attr('src', '/static/image/QR Code 400.svg')
        copyToClipboard('00020126990014BR.GOV.BCB.PIX0114650851360001970259Valor referente a anuidade como membro associado e/ou titul5204000053039865406400.005802BR5904SBOP6009SAO PAULO622505218gOyl59TrT3LUh1fuyTln63047347')
    }

}

const _get_member = setInterval(() => {
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
                        } catch { }
                    }
                }

                membro.exists = true;
                console.log(membro);

                if (membro.adm) {
                    $('.adm-button').css('visibility', 'visible');
                    $('.adm-button').on('click', () => {
                        window.location.href = '/adm/';
                    });
                }

                if (membro.pago) {
                    $('#upgrade-plan-button').on('click', (event) => {
                        if (membro.assinatura == 'Associado') {
                            if ($('.selected-plan').attr('id')) {
                                $('.vigencia-container').toggle()
                                $('.documents-container').fadeToggle();
                            } else {
                                $('.plans-panel').fadeOut(0, () => {
                                    $('.payment-container').fadeIn();
                                    tipoPagamento($('.active-plan').attr('id'))
                                });
                            }

                            if (mobile) {
                                $('.plans-panel').hide();
                                window.scrollTo(0, 0);
                            }

                        }
                    });
                } else {
                    $('.plans').on('click', (event) => {
                        $('.selected-plan').removeClass('selected-plan');
                        $(event.target).closest('.plans').addClass('selected-plan');
                        $('#upgrade-plan-button').removeClass('deactivated-button');

                    })

                    $('#upgrade-plan-button').on('click', () => {
                        $('.plans-panel').fadeOut(0, () => {
                            $('.payment-container').fadeIn();
                            tipoPagamento($('.active-plan').attr('id'))
                        });
                    })

                    

                }

                if (!(membro.assinatura == 'Associado')) {
                    $('.plans').on('click', (event) => {
                        if ($(event.target).closest('.plans').attr('id') == 'titular') {
                            // $('#upgrade-plan-button').addClass('deactivated-button');
                        }
                    })

                    $('#upgrade-plan-button').on('click', () => {
                        $('.plans-panel').fadeOut(0, () => {
                            $('.payment-container').fadeIn();
                            if ($('.selected-plan').attr('id')) {
                                tipoPagamento($('.selected-plan').attr('id'))
                            } else {
                                tipoPagamento($('.active-plan').attr('id'))
                            }
                        });
                    })

                    // $('.back-button').on('click', () => {
                    //     $('.payment-container').fadeOut(0, () => {
                    //         $('.plans-panel').fadeIn();
                    //     })
                    // })


                }

                if (!membro.assinatura) {
                    $('#toolbar-restrict').css('opacity', '0.5');
                    $('#toolbar-restrict').css('pointer-events', 'none');
                    $('#toolbar-requests').css('opacity', '0.5');
                    $('#toolbar-requests').css('pointer-events', 'none');

                    $('#vigencia-text').text('Pagamento não confirmado');
                    $('.vigencia-container').css('background-color', 'var(--borda-plano-vencido)');

                    if (!membro.temporario) $('#toolbar-plans').trigger('click');
                }
            });
        }, 100)
        clearInterval(_get_member);

    }
}, 100);

$('.back-button').on('click', () => {
    $('.payment-container').fadeOut(0, () => {
        $('.plans-panel').fadeIn();
    })
})


/* MOBILE STYLING */
$('#menu-button').on('click', () => {
    $('.body-toolbar').fadeToggle();
})
if (mobile) {

    $('.body-container').hide()

    $('.toolbar').on('click', () => {
        $('.body-toolbar').fadeToggle();
    })
    $('.body-toolbar').toggle();

    $('#plans-cancel-button').on('click', () => {
        $('.plans-panel').fadeIn('slow');
    })
}
