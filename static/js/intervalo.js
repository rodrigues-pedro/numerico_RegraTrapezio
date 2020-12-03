const xInicial = document.querySelector('#x_o');
const xFinal = document.querySelector('#x_f');
const calcular = document.querySelector('#btn-submit');

calcular.addEventListener('click',function(){
    if(xInicial.value > xFinal.value){
        alert('O valor inicial do intervalo não pode ser maior que o final. Por favor, reescreva o intervalo');
        xInicial.value = '';
        xFinal.value = '';
        document.reload(false);
    }
    console.log(xInicial.textContent)
});

$("#form").submit(function() {
    if($("#x_o").val()== null || $("#x_f").val() =="" || $("#function").val() == "" || $("#erro_n").val() == ""){
        return false;
    }
});
