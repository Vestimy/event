from flask import Blueprint, request, render_template, redirect, abort
from event import logger, config, allowed_photo_profile, allowed_document_profile, load_user
from event.emails import send_confirm, send_forgot, send_confirm_succes
from event import generate_id
from flask_login import logout_user, login_user, login_required, current_user
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from event.forms import *

security = Blueprint('security', __name__)


@security.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('security.login'))


@security.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
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
        if user.active:
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
        else:
            flash('Пользователь не активирван')
    return render_template('security/login_user.html', login_user_form=login_user_form)


@security.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User()
    register_user_form = RegisterUserForm(request.form, obj=user)
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    id = request.args.get('id')
    email = request.args.get('email')
    if id and email:
        register_user_form = RegisterInviteForm(request.form, obj=user)
        invite = Invite.query.filter(Invite.invite_id == id).first()
        if request.method == 'POST' and request.form.get(
                'submit_invite') and invite and invite.email == email:
            if register_user_form.validate():
                if not (login or password or password_confirm):
                    flash('Заполните все поля')
                elif password != password_confirm:
                    flash('Пароли не совпадают')
                else:
                    register_user_form.populate_obj(user)
                    hash_pwd = generate_password_hash(password)
                    user.password = hash_pwd
                    user.email = invite.email
                    user.active = True
                    db.session.add(user)

                    user.company.append(Company.query.get(invite.company_id))
                    settings = Settings(company_default_id=invite.company_id)
                    settings.users.append(user)
                    db.session.add(settings)
                    db.session.delete(invite)
                    db.session.commit()
                    # html = render_template('email_templates/action.html', user=user, id=id, password=password)
                    # send_confirm(user.email, html)
                return redirect(url_for('security.login'))
        return render_template('security/register_invite.html', register_user_form=register_user_form)
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

            id = generate_id()
            confirmation = Confirmation(email=user.email, conf_id=id)
            db.session.add(confirmation)
            db.session.commit()

            html = render_template('email_templates/action.html', user=user, id=id, password=password)
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


@security.route('/confirmation', methods=['GET', 'POST'])
def confirmation():
    company = Company()
    form = CompanyForm(request.form, obj=company)
    email = request.args.get('email')
    id = request.args.get('id')
    if email and id:
        conf_id = Confirmation.query.filter(Confirmation.conf_id == id).first()
        if conf_id and conf_id.email == email:
            user = User.query.filter(User.email == conf_id.email).first()
            if request.method == 'POST':
                form.populate_obj(company)
                db.session.add(company)
                company.creator_id = user.id
                try:
                    company.staff.append(user)
                    company.user_admin.append(user)
                    db.session.commit()
                except Exception as e:
                    logger.warning(
                        f'Подвержение почты: {e}'
                    )
                if company:
                    db.session.delete(conf_id)
                    user.active = True
                    settings = Settings(company_default_id=company.id)
                    settings.users.append(user)
                    db.session.add(settings)
                    db.session.commit()
                html = render_template('email_templates/confirm_successful.html', user=user)
                send_confirm_succes(user.email, html)
                return redirect(url_for('security.login'))
            return render_template('security/confirmation.html', form=form)
    return abort(404)


@security.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('security.login') + '?2next=' + request.url)
    return response
