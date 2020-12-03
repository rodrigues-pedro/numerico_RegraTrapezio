const btn = document.querySelector('#sintaxe');

btn.addEventListener('click', function() {
    const modal = document.querySelector('#modal--instrucoes');
    modal.classList.add('mostrar');

    const btnFechar = document.querySelector('#btn--fechar');
    modal.addEventListener('click', function(evento) {
        if(evento.target == modal || evento.target == btnFechar){
            modal.classList.remove('mostrar');
        }
    });
});