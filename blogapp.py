from flask import Flask

app = Flask(__name__)

app.config.from_pyfile('settings.py')

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

db.init_app(app)

from flask_migrate import Migrate
Migrate(app,db)

from sqlalchemy import select
from apps import models
from flask import render_template
from flask import request
from flask_paginate import Pagination,get_page_parameter



@app.route('/')
def index():

    stmt = select(models.Blogpost).order_by(models.Blogpost.id.desc())

    entries = db.session.execute(stmt).scalars().all()

    page = request.args.get(get_page_parameter(),type=int,default=1)

    res = entries[(page - 1)*3:page*3]

    pagination = Pagination(page=page,total=len(entries),per_page=3)

    return render_template('index.html',rows=res,pagination=pagination)

@app.route('/entries/<int:id>')
def show_entry(id):

    entry = db.session.get(models.Blogpost,id)

    return render_template('ppost.html',entry=entry)

from flask import url_for,redirect
from apps import forms
from flask import flash

@app.route('/contact',methods=['GET','POST'])
def contact():
    form = forms.InquiryForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        message = form.message.data

        send_mail(
            to = 'kazu06125420@gmail.com',
            subject = "問い合わせページからのメッセージ",
            template = "send_mail.txt",
            username = username,
            email = email,
            message = message
        )

        flash('お問い合わせの内容は送信されました。')

        return redirect(url_for('contact_complete'))
    
    return render_template('contact.html',form=form)

@app.route('/contact_complete')
def contact_complete():
    return render_template('contact_complete.html')

from flask_mail import Mail
mail = Mail(app)

from flask_mail import Message
def send_mail(to,subject,template,**kwargs):

    msg = Message(subject,recipients=[to])
    msg.body = render_template(template,**kwargs)

    mail.send(msg)



from apps.crud.views import crud

app.register_blueprint(crud)



