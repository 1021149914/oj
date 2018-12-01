from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user ,logout_user
from app.models import User, Info, Problem, Commit
from flask import request
from werkzeug.urls import url_parse
from flask_login import login_required
from app import db
from app.forms import RegistrationForm, InfoForm, AProblem, SProblem, Submission
from werkzeug import generate_password_hash, check_password_hash
import os
import datetime

def save_to_file(file_name,contents):
    fh=open(file_name,'w')
    fh.write(contents)
    fh.close()

def read_file(file_name):
    if os.path.exists(file_name):
        fh=open(file_name,'r')
        contents=fh.read()
        return contents
    return ""

@app.route('/')
@app.route('/index')
def index():
    info=Info.query.order_by(Info.Infoid.desc())
    data=[]
    for i in info:
        tmp={}
        tmp['id']=i.Infoid
        tmp['title']=i.Infotitle
        file_name='./Info/info'+str(i.Infoid)+'.txt'
        tmp['content']=read_file(file_name)
        data.append(tmp)
    return render_template('index.html', title='Home', data=data)

@app.route('/problem')
def problem():
    problem=Problem.query.order_by(Problem.problemid)
    data=[]
    for i in problem:
        tmp={}
        tmp['id']=i.problemid
        file_name='./Problem/problem'+str(i.problemid)
        tmp['title']=read_file(file_name+'title.txt')
        tmp['source']=read_file(file_name+'source.txt')
        data.append(tmp)
    return render_template('problem.html',title='Problem', data=data)

@app.route('/detail/<name>',methods=['GET','POST'])
def detial(name):
    tmp={}
    problem=Problem.query.filter_by(problemid=name).first()
    file_name='./Problem/problem'+str(name)
    tmp['title']=read_file(file_name+'title.txt')
    tmp['description']=read_file(file_name+'description.txt')
    tmp['input']=read_file(file_name+'input.txt')
    tmp['output']=read_file(file_name+'output.txt')
    tmp['sampleinput']=read_file(file_name+'sampleinput.txt')
    tmp['sampleoutput']=read_file(file_name+'sampleoutput.txt')
    tmp['hint']=read_file(file_name+'hint.txt')
    tmp['source']=read_file(file_name+'source.txt')
    tmp['ms']=problem.problemms
    tmp['kb']=problem.problemkb
    tmp['id']=problem.problemid
    tk='Problem'+str(name)
    form=SProblem()
    if form.validate_on_submit():
        return redirect(url_for('submission'))
    return render_template('detial.html',title=tk,tmp=tmp,form=form)

@app.route('/submission',methods=['GET','POST'])
def submission():
    form = Submission()
    if form.validate_on_submit():
        status=form.status.data
        problemid=form.problemid.data
        rows=Commit.query.count()
        commit=Commit(commitid=rows+1,userid=current_user.userid,problemid=problemid)
        file_name='./Submit/'+str(rows)
        if int(status)==0:file_name=file_name+'.cpp'
        if int(status)==1:file_name=file_name+'.java'
        if int(status)==2:file_name=file_name+'.py'
        save_to_file(file_name,form.code.data)
        flash('Congratulations, you have submit you code!')
        commit.committime=datetime.datetime.now()
        commit.commitans="Accepted"
        commit.commitms=120
        commit.commitkb=1024
        db.session.add(commit)
        db.session.commit()
        return redirect(url_for('submission'))
    return render_template('submission.html',title='Submit Problem',form=form)
    


@app.route('/contest')
def contest():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@app.route('/status') 
def status():
    commit=Commit.query.order_by(Commit.commitid.desc())
    data=[]
    for i in commit:
        tmp={}
        tmp['id']=i.commitid
        tmp['problemid']=i.problemid
        tmp['time']=i.committime
        file_name='./Problem/problem'+str(i.problemid)
        tmp['title']=read_file(file_name+'title.txt')
        tmp['ans']=i.commitans
        tmp['ms']=i.commitms
        tmp['kb']=i.commitkb
        data.append(tmp)
    return render_template('status.html', title='Home', data=data)

@app.route('/rank')
def rank():
    user=User.query.all()
    data=[]
    for i in user:
        length=Commit.query.filter_by(userid=i.userid).count()
        tmp=[]
        tmp.append(i.userid)
        tmp.append(i.username)
        tmp.append(length)
        data.append(tmp)
    data.sort(key=lambda x:x[2])
    data.reverse()
    return render_template('rank.html',title='Rank',data=data)

    

@app.route('/addproblem',methods=['GET','POST'])
@login_required
def addproblem():
    form = AProblem()
    if form.validate_on_submit():
        problem=Problem(problemms=form.problemms.data,problemkb=form.problemkb.data)
        db.session.add(problem)
        db.session.commit()
        flash('Congratulations, the problem has been added!')
        rows=Problem.query.count()
        url='./Problem/problem'+str(rows)
        save_to_file(url+'title.txt',form.problemtitle.data)
        save_to_file(url+'description.txt',form.problemdescription.data)
        save_to_file(url+'input.txt',form.probleminput.data)
        save_to_file(url+'output.txt',form.problemoutput.data)
        save_to_file(url+'sampleinput.txt',form.problemsampleinput.data)
        save_to_file(url+'sampleoutput.txt',form.problemsampleoutput.data)
        save_to_file(url+'hint.txt',form.problemhint.data)
        save_to_file(url+'source.txt',form.problemsource.data)
        form.problemtest.data.save(url+'test.in')
        form.problemans.data.save(url+'ans.out')
        return redirect(url_for('index'))
    return render_template('addproblem.html',title='Add Problem',form=form)

@app.route('/inform',methods=['GET','POST'])
@login_required
def inform():
    form = InfoForm()
    if form.validate_on_submit():
        info=Info(Infotitle=form.infotitle.data)
        db.session.add(info)
        db.session.commit()
        flash('Congratulations, the infomation has been added!')
        #info=Info.query.filter_by(Infotitle=form.infotitle.data).first()
        rows=Info.query.count()
        url='./Info/info'+str(rows)+'.txt'
        save_to_file(url,form.infocontent.data)
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

