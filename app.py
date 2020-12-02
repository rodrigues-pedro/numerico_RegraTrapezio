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

x, w = symbols('x w')

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)

class Func(FlaskForm):
    function = StringField('Função à ser Integrada', validators=[DataRequired()])
    x_o = DecimalField('Valor inicial do Intervalo', validators=[DataRequired()])
    x_f = DecimalField('Valor final do Intervalo', validators=[DataRequired()])
    erro_n = DecimalField('Erro ou Número de Trapézios', validators=[DataRequired()])
    submit = SubmitField('Calcular', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def funcPlot():
    form = Func()
    if request.method == 'POST':
        if request.form.get("btn-submit", False) == 'submit':
            func = parse_expr(form.function.data)
            x_o = float(form.x_o.data)
            x_f = float(form.x_f.data)
            erro_n = float(form.erro_n.data)

            if erro_n >= 1:
                n = int(np.ceil(erro_n))
                area = resourses.calculoArea(func, x_o, x_f, n)
                erro = resourses.calculoErro(func, x_o, x_f, n)
            else:
                n = resourses.calculoN(func, x_o, x_f, erro_n)
                area = resourses.calculoArea(func, x_o, x_f, n)
                erro = erro_n

            areaReal = resourses.integralDefinida(func, x_o, x_f)

            fig = resourses.trapezioPlot(func, x_o, x_f, n) 

            # Convert plot to PNG image
            pngImage = io.BytesIO()
            FigureCanvas(fig).print_png(pngImage)
            
            # Encode PNG image to base64 string
            grafico = "data:image/png;base64,"
            grafico += base64.b64encode(pngImage.getvalue()).decode('utf8')

            try:
                erroReal = abs(areaReal - area)      
                return render_template('results.html', i=0, erro="{:.5f}".format(erro), area="{:.5f}".format(area), 
                                                    areaReal="{:.5f}".format(areaReal),erroReal="{:.5f}".format(erroReal),
                                                    func=str(func), grafico=grafico, n=n)
            except:
                erroReal = areaReal
                return render_template('results.html', i=0, erro="{:.5f}".format(erro), area="{:.5f}".format(area), 
                                                    areaReal="{}".format(areaReal),erroReal="{}".format(erroReal),
                                                    func=str(func), grafico=grafico, n=n)
    return render_template('index.html', form=form)

@app.route('/verificar_formula', methods=['GET'])
def verificar_formula():

    func = parse_expr(request.args.get('formula'))
    x_o = float(request.args.get('x_o'))
    x_f = float(request.args.get('x_f'))
    print(func, type(func))
    print(x)
    result = resourses.verifica_continuidade(func, x_o, x_f)

    return result

if __name__ == "__main__":
    app.run(debug=True)