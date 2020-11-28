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
    erro_n = DecimalField('Valor inicial do Intervalo', validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def newPost():
    form = NewPost()
    post = {}
    i = 1
    if form.validate_on_submit():
        i = 0
        flash('New post from {}, titled {}'.format(form.author.data, form.title.data))
        postTitle = form.title.data
        postContent = form.content.data
        postAuthor = form.author.data
        post = {'title': form.title.data,'content': form.content.data,'author': form.author.data}
        config.add_post(postTitle, postContent, postAuthor)
        return render_template('newPost.html', form=form, post=post, i=i)
    return render_template('newPost.html', form=form, post=post, i=i)

if __name__ == "__main__":
    app.run(debug=True)