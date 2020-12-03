function  iniciaModal(modalID) {
    const modal = document.getElementById(modalID);
    if(modal){
        modal.classList.add('mostrar');
        modal.addEventListener('click', (evento) => {
            if(evento.target.Id == modalID || evento.target.className == 'btn--fechar'){
                modal.classList.remove('mostrar')
            }
        });
    }
}

const modalSintaxe = document.querySelector('.cabecalho');
modalSintaxe.addEventListener('click', iniciaModal('modal--instrucoes'));