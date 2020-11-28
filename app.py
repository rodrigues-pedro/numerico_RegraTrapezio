from flask import Flask, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired
import config
import os

app = Flask(__name__)
app.config.from_object(config.Config)

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
        func = parsing.sympy_parser.parse_expr(form.function.data)
        x_o = form.x_o.data
        x_f = form.x_f.data
        erro_n = form.erro_n.data
        if erro_n >= 1:
            n = erro_n
        else:
            erro = erro_n
        

        return render_template('index.html', form=form, post=post, i=i)
    return render_template('index.html', form=form, post=post, i=i)

if __name__ == "__main__":
    app.run(debug=True)