from flask import Blueprint

crud = Blueprint('crud',__name__,template_folder='templates',static_folder='static_crud')

from flask import render_template,url_for,redirect,session
from apps.crud import forms
from apps.blogapp import app

@crud.route('/admincreate',methods=['GET','POST'])
def login():
    form = forms.AdminForm()
    session['logged_in'] = False

    if form.validate_on_submit():

        if form.username.data != app.config['USERNAME']\
        or form.password.data != app.config['PASSWORD']:
            
            return render_template('login.html',form=form)
        
        else:
            session['logged_in'] = True
            return redirect(url_for('crud.article'))
        
    return render_template('login.html',form=form)

from apps import models
from apps.blogapp import db

@crud.route('/post',methods=['GET','POST'])
def article():

    if not session.get('logged_in'):
        return redirect(url_for('crud.login'))
    
    form_art = forms.ArticlePost()

    if form_art.validate_on_submit():
        blogpost = models.Blogpost(
            title=form_art.post_title.data,
            contents=form_art.post_contents.data,
        )

        db.session.add(blogpost)
        db.session.commit()

        session.pop('logged_in',None)

        return redirect(url_for('crud.login'))
    
    return render_template('post.html',form=form_art)


@crud.route('/admindelete',methods=['GET','POST'])
def login_del():
    form = forms.AdminForm()
    session['logged_in'] = False

    if form.validate_on_submit():

        if form.username.data != app.config['USERNAME']\
        or form.password.data != app.config['PASSWORD']:
            
            return render_template('login_delete.html',form=form)
        
        else:
            session['logged_in'] = True
            return redirect(url_for('crud.delete_entry'))
        
    return render_template('login_delete.html',form=form)

from sqlalchemy import select

@crud.route('/delete',methods=['GET','POST'])
def delete_entry():

    if not session.get('logged_in'):
        return redirect(url_for('crud.login_del'))
    
    stmt = select(models.Blogpost).order_by(models.Blogpost.id.desc())

    entries = db.session.execute(stmt).scalars().all()

    return render_template('delete.html',entries=entries)

@crud.route('/delete/<int:id>')
def delete(id):

    entry = db.session.get(models.Blogpost,id)

    db.session.delete(entry)

    db.session.commit()

    session.pop('logged_in',None)

    return redirect(url_for('crud.login_del'))

    























        

    
