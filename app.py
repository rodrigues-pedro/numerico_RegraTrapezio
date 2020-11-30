from flask import Flask, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
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
app.debug = True

class Func(FlaskForm):
    function = StringField('Função à ser Integrada', validators=[DataRequired()])
    x_o = DecimalField('Valor inicial do Intervalo', validators=[DataRequired()])
    x_f = DecimalField('Valor final do Intervalo', validators=[DataRequired()])
    erro_n = DecimalField('Erro ou Número de Trapézios', validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])

erro_n = 0.
erro = 0.
n = 0
area = 0.
x_o = 0.
x_f = 0.
func = 0*x

@app.route('/', methods=['GET', 'POST'])
def funcPlot():
    form = Func()
    if form.validate_on_submit():
        func = parse_expr(form.function.data)
        x_o = float(form.x_o.data)
        x_f = float(form.x_f.data)
        erro_n = float(form.erro_n.data)

        if erro_n >= 1:
            n = int(np.around(erro_n, 0))
            area = resourses.calculoArea(func, x_o, x_f, n)
            erro = resourses.calculoErro(func, x_o, x_f, n)
        else:
            n = resourses.calculoN(func, x_o, x_f, erro_n)
            area = resourses.calculoArea(func, x_o, x_f, n)
            erro = erro_n

        fig = resourses.trapezioPlot(func, x_o, x_f, n) 

        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        
        # Encode PNG image to base64 string
        grafico = "data:image/png;base64,"
        grafico += base64.b64encode(pngImage.getvalue()).decode('utf8')
      
        return render_template('results.html', i=0, erro_n=erro_n, n=n, erro=erro, area=area, x_o=x_o,
                                            x_f=x_f, func=str(func), grafico=grafico)
    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)