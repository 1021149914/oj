from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user ,logout_user
from app.models import User, Info
from flask import request
from werkzeug.urls import url_parse
from flask_login import login_required
from app import db
from app.forms import RegistrationForm, InfoForm
from werkzeug import generate_password_hash, check_password_hash

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/problem')
def problem():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@app.route('/contest')
def contest():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@app.route('/status')
def status():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@app.route('/rank')
def rank():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@app.route('/inform',methods=['GET','POST'])
@login_required
def inform():
    form = InfoForm()
    if form.validate_on_submit():
        info=Info(Infotitle=form.infotitle.data)
        db.session.add(info)
        db.session.commit()
        flash('Congratulations, the infomation has been added!')
        return redirect(url_for('index'))
    return render_template('inform.html',title='Information', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, useremail=form.useremail.data)
        user.userpassword=generate_password_hash(form.password.data)
        user.userp=0
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not check_password_hash(user.userpassword,form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

