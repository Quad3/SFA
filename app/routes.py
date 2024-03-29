from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from flask_login import login_required

from app import app
from app import db

from app.forms import LoginForm, RegistrationForm
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('index'))
		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('index'))
	return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congrats, you are now a registered user')
		return redirect(url_for('login'))
	return render_template('register.html', title='Registration', form=form)

