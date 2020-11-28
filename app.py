from flask import Flask, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired
from sympy.parsing.sympy_parser import parse_expr
import config
import numpy as np
import os

app = Flask(__name__)
app.config.from_object(config.Config)
app.debug = True

class Func(FlaskForm):
    function = StringField('Função à ser Integrada', validators=[DataRequired()])
    x_o = DecimalField('Valor inicial do Intervalo', validators=[DataRequired()])
    x_f = DecimalField('Valor final do Intervalo', validators=[DataRequired()])
    erro_n = DecimalField('Erro ou Número de Trapézios', validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def newPost():
    form = Func()
    post = {}
    i = 1
    if form.validate_on_submit():
        i = 0
        func = parse_expr(form.function.data)
        x_o = form.x_o.data
        x_f = form.x_f.data
        erro_n = form.erro_n.data

        if erro_n >= 1:
            n = int(np.around(erro_n, 0))
            area = config.calculoArea(func, x_o, x_f, n)
            erro = config.calculoErro(func, x_o, x_f, n)
        else:
            n = config.calculoN(func, x_o, x_f, erro_n)
            area = config.calculoArea(func, x_o, x_f, n)
            erro = erro_n

        grafico = config.trapezioPlot(func, x_o, x_f, n)       

        return render_template('index.html', form=form, area=area, erro=erro, n=n, grafico=grafico, erro_n=erro_n)
    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)