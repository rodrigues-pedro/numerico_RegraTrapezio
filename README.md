# numerico_RegraTrapezio
Trabalho de cálculo numérico, implementação do método dos trapézios para o cálculo de integrais definidas.

Link para usar o site:
https://flask-regratrapezio.herokuapp.com/
* Não sabemos quão bom vão ser os servidores, se estiver dando muito erro pode ser por sobrecarga, considerando que usamos uma plataforma gratuita e aberta para o host.

Foram usados no front-end: html, css, js; e no back-end: python com flask  

Qualquer bug pode ser avisado atravéz da sessão "issues" do própio GitHub, ou por email nos institucionais: 
Pedro: "rodrigues.pedro@discente.ufg.br"
Murilo: "santosmurilo@discente.ufg.br"
Igor: "igoralves@discente.ufg.br"

Para rodar localmente recomendamos o uso de um Virtual Enviroment,no caso do Python >= 3.4:

É simples, rode no terminal, dentro da pasta com os arquivos:

Isso criará o Virtual Enviroment:
python -m venv venv 
ou
python3 -m venv venv
(dependendo do estado de instalação do python)

Agora é nescessário ativar o venv:
Windows:
venv/Scripts/activate
Linux/Mac:
source venv/bin/activate

e ai instale os requerimentos:
pip install -r requirements.txt

Agora é só rodar, usando o comando:
flask run
