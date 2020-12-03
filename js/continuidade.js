 // adiciona um id ao botao de adicionar coluans
 botoes = document.querySelectorAll("button")
 $("#btn-submit").attr("disabled",true);

 $("#checar_formula").click(function () {
     var formula = document.getElementById('function').value;
     var x_o = document.getElementById('x_o').value;
     var x_f = document.getElementById('x_f').value;

     console.log("formula: ",formula);
     console.log("x_o: ",x_o);
     console.log("x_f: ",x_f);
         
     $.ajax({
         url: "{{url_for('verificar_formula')}}?formula=" + formula+ "&x_o=" + x_o+ "&x_f=" + x_f,
         success: function (result) {
         var verify = document.getElementById('verifica_formula');

             if(result=='1'){
                 alert('Intervalo Válido, Prossiga')
                 $("#btn-submit").attr("disabled",false);
             }else{
                 alert(result)
             }
         }
     });
     
 });