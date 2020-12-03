const xInicial = document.querySelector('#x_0');
const xFinal = document.querySelector('#x_f');
const calcular = document.querySelector('#btn-submit');

calcular.addEventListener('click',function(){
    if(xInicial.value > xFinal.value){
        alert('O valor inicial do intervalo não pode ser maior que o final. Por favor, reescreva o intervalo');
        xInicial.textContent = '';
        xFinal.textContent = '';
    }
});
