const main = async () => {
    let button = document.querySelector('#submit_button')
    let input_num_pregao = document.querySelector('#input_num_pregao')
    button.addEventListener('click', () => {
        if (input_num_pregao.value){
            const openCoder = async () => {
                window.call.openMainPy(input_num_pregao.value)
            }
            openCoder()
        }
    })

    // Expandir
    document.querySelector('.btn-expand').addEventListener('click', () => {
        window.call.expand_screen()
        let element = document.querySelector('.btn-expand');
        if (element.getAttribute('data-clicked') == 'true'){
            element.setAttribute('data-clicked', 'false');
        }else{
            element.setAttribute('data-clicked', 'true');
        }
    })

    // Fechar o App
    document.querySelector('.close').addEventListener('click', () => {
        window.call.close()
    })

    // minimizar o App
    document.querySelector('.minimize').addEventListener('click', () => {
        window.call.minimize()
    })
}

main()