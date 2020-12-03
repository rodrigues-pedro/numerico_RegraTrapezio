from flask import Flask, render_template, url_for, flash, redirect, request
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired
from sympy.parsing.sympy_parser import parse_expr
from config import Config
import resourses
from sympy import *
import numpy as np
import os
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

#define as variáveis à serem usadas
x, w = symbols('x w')

#inicia a instancia do Flask como app, ajusta configurações
app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)

#define a classe do formulário para input do usuário
class Func(FlaskForm):
    function = StringField('Função à ser Integrada', validators=[DataRequired()])
    x_o = DecimalField('Valor inicial do Intervalo', validators=[DataRequired()])
    x_f = DecimalField('Valor final do Intervalo', validators=[DataRequired()])
    erro_n = DecimalField('Erro ou Número de Trapézios', validators=[DataRequired()])
    submit = SubmitField('Calcular', validators=[DataRequired()])

#define a rota do URL do form
@app.route('/', methods=['GET', 'POST'])
def funcPlot():
    #define instancia do form
    form = Func()
    if request.method == 'POST':
        #ao receber o envio dos dados
        if request.form.get("btn-submit", False) == 'submit':
            #recebe os dados e adequa os formatos de acordo com os eperados para cada função
            func = parse_expr(form.function.data)
            x_o = float(form.x_o.data)
            x_f = float(form.x_f.data)
            erro_n = float(form.erro_n.data)

            #se o valor de erro_n for maior que 1 o consideraremos como número de trapézios
            if erro_n >= 1:
                #adequa o valor de n
                n = int(np.ceil(erro_n))
                #calcula a area
                area = resourses.calculoArea(func, x_o, x_f, n)
                #estima o erro 
                erro = resourses.calculoErro(func, x_o, x_f, n)
            #caso for menor consideraremos como erro máximo
            else:
                #calcula o n para aceitar que o erro seja <= que o erro máximo
                n = resourses.calculoN(func, x_o, x_f, erro_n)
                #calcula a area
                area = resourses.calculoArea(func, x_o, x_f, n)
                #coloca o erro na variavel correta
                erro = erro_n

            #calcula a area real da integral
            areaReal = resourses.integralDefinida(func, x_o, x_f)
            #realiza o gráfico
            fig = resourses.trapezioPlot(func, x_o, x_f, n) 

            #converte o gráfico em PNG
            pngImage = io.BytesIO()
            FigureCanvas(fig).print_png(pngImage)
            
            #decodifica a imagem PNG para base64 string
            grafico = "data:image/png;base64,"
            grafico += base64.b64encode(pngImage.getvalue()).decode('utf8')
            
            #se o valor da integral real existir calcula o erro real e envia tudo para a página dos resultados
            try:
                erroReal = abs(areaReal - area)      
                return render_template('results.html', i=0, erro="{:.5f}".format(erro), area="{:.5f}".format(area), 
                                                    areaReal="{:.5f}".format(areaReal),erroReal="{:.5f}".format(erroReal),
                                                    func=str(func), grafico=grafico, n=n)
            #caso contrário,envia uma mensagem da impossiblidade do cálculo da integral e 
            #e os valores calculados para a página dos resultados
            except:
                erroReal = areaReal
                return render_template('results.html', i=0, erro="{:.5f}".format(erro), area="{:.5f}".format(area), 
                                                    areaReal="{}".format(areaReal),erroReal="{}".format(erroReal),
                                                    func=str(func), grafico=grafico, n=n)
    return render_template('index.html', form=form)

#faz a verificação da continuidade da fórmula
@app.route('/verificar_formula', methods=['GET'])
def verificar_formula():
    #recebe os dados
    func = parse_expr(request.args.get('formula'))
    x_o = float(request.args.get('x_o'))
    x_f = float(request.args.get('x_f'))
    #verifica a continuidade
    result = resourses.verifica_continuidade(func, x_o, x_f)
    #envia os resultados para o js dar os prosseguimentos
    return result

if __name__ == "__main__":
    app.run(debug=True)