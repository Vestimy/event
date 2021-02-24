from logging import log
import os
from re import I
from flask import Blueprint, jsonify, request, render_template, redirect, abort
from flask.wrappers import Response
from flask_security.utils import hash_password
from werkzeug.exceptions import RequestTimeout
from event import logger, config, allowed_photo_profile, allowed_document_profile, load_user, send_confirm, send_forgot

from flask_login import logout_user, login_user, login_required, current_user
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from event import send_msg
from event.forms import *

security = Blueprint('security', __name__)

@security.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@security.route('/login', methods=['GET', 'POST'])
def login():
    login_user_form = LoginForm(request.form)
    email = request.form.get('email')
    password = request.form.get('password')
    if request.method == 'POST' and login_user_form.validate():
        user = User.get_email(email)
        if check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page is None:
                return redirect(url_for('main.index'))
            return redirect(next_page)
        else:
            flash('Неверый логин или пароль')
    return render_template('security/login_user.html', login_user_form=login_user_form)


@security.route('/register', methods=['GET', 'POST'])
def register():
    user = User()
    register_user_form = RegisterUserForm(request.form, obj=user)
    email = request.form.get('email')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')

    if request.method == 'POST' and register_user_form.validate():
        if not (login or password or password2):
            flash('Заполните все поля')
        elif password != password_confirm:
            flash('Пароли не совпадают')
        else:
            register_user_form.populate_obj(user)
            hash_pwd = generate_password_hash(password)
            user.password = hash_pwd
            db.session.add(user)
            db.session.commit()
        html = render_template('email_templates/action.html', user=user, password=password)
        
        
        send_confirm(user.email, html)
        return redirect(url_for('security.login'))
    return render_template('security/register_user.html', register_user_form=register_user_form)

@security.route('/reset', methods=['GET', 'POST'])
def reset():
    form = ForgotPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.email == request.form.email.get('email')).first()
        html = render_template('email_templates/action.html', user=user)
        send_forgot(request.form.get('email', html))
    return render_template('security/forgot_password.html', forgot_password_form=form)

@security.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('security.login')+'?2next='+request.url)

    return response