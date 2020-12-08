const xInicial = document.querySelector('#x_o');
const xFinal = document.querySelector('#x_f');
const calcular = document.querySelector('#btn-submit');

calcular.addEventListener('click',function(){
    console.log(xInicial.textContent)
    console.log(xInicial.value)
    console.log(typeof(xInicial.value))
    console.log(xFinal.value)
    console.log(typeof(xFinal.value))
    if(Number(xInicial.value) > Number(xFinal.value)){
        alert('O valor inicial do intervalo não pode ser maior que o final. Por favor, reescreva o intervalo');
        xInicial.value = '';
        xFinal.value = '';
        document.reload(false);
    }
});

$("#form").submit(function() {
    if($("#x_o").val()== null || $("#x_f").val() =="" || $("#function").val() == "" || $("#erro_n").val() == ""){
        return false;
    }
});
