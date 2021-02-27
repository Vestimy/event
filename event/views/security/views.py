from flask import Blueprint, request, render_template, redirect, abort
from event import logger, config, allowed_photo_profile, allowed_document_profile, load_user
from event import send_confirm, send_forgot
from flask_login import logout_user, login_user, login_required, current_user
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from event import send_msg
from event.forms import *
import uuid

security = Blueprint('security', __name__)


def conf_id():
    return str(uuid.uuid4())


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
        if User.get_email(email):
            user = User.get_email(email)
        elif User.query.filter(User.login == email).first():
            user = User.query.filter(User.login == email).first()
        else:
            user = None
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                next_page = request.args.get('next')
                if next_page is None:
                    return redirect(url_for('main.index'))
                return redirect(next_page)
            else:
                flash('Неверый логин или пароль')
        else:
            flash('Пользователь не существует')
    return render_template('security/login_user.html', login_user_form=login_user_form)


@security.route('/register', methods=['GET', 'POST'])
def register():
    user = User()
    register_user_form = RegisterUserForm(request.form, obj=user)
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')

    if request.method == 'POST' and register_user_form.validate():
        if not (login or password or password_confirm):
            flash('Заполните все поля')
        elif password != password_confirm:
            flash('Пароли не совпадают')
        else:
            register_user_form.populate_obj(user)
            hash_pwd = generate_password_hash(password)
            user.password = hash_pwd
            db.session.add(user)

            id = conf_id()
            confirmation = Confirmation(user.email, id)
            db.session.add(confirmation)
            db.session.commit()

            html = render_template('email_templates/action.html', user=user,id=id, password=password)
            send_confirm(user.email, html)
        return redirect(url_for('security.login'))
    return render_template('security/register_user.html', register_user_form=register_user_form)


@security.route('/reset', methods=['GET', 'POST'])
def reset():
    form = ForgotPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.email == request.form.get('email')).first()
        html = render_template('email_templates/action.html', user=user)
        send_forgot(request.form.get('email'), html)
    return render_template('security/forgot_password.html', forgot_password_form=form)


@security.route('/tests', methods=['GET', 'POST'])
def tests():
    return render_template('register_test.html')


@security.route('/confirmation', methods=['GET'])
def confirmation():
    # print(request.host_url + url_for('security.confirmation', email='vestimyandrey@gmail.com', id='21421421421412'))
    email = request.args.get('email')
    id = request.args.get('id')
    return render_template('security/confirmation.html')


@security.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('security.login') + '?2next=' + request.url)
    return response
