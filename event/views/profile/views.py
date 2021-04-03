from flask import Blueprint, jsonify, request, json, render_template, redirect
from flask import abort
from event import logger, config, allowed_photo_profile
import os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_security import login_required, current_user
from event.decorators import decorated_admin
from event.forms import *

profiles = Blueprint('profiles', __name__)


@profiles.route('/profile/', methods=['GET'])
@login_required
def profile_all():
    if current_user.is_authenticated:
        id = current_user.id
        user = User.query.get(id)
        return redirect(url_for('main.profile', id=id))
    return redirect(url_for('security.login'))


@profiles.route('/profile/<int:id>', methods=['GET', "POST"])
@login_required
def profile(id, page=1):
    per_page = 10
    user = User.query.get(id)
    send_message = SendMessageForm(request.form)
    if user:
        form = ProfileImg(request.form, obj=user)
        page = request.args.get('page', type=int, default=1)
        page_event = request.args.get('page_event', type=int, default=1)
        events = Event.query.filter(Event.user_id == user.id).order_by(Event.date_event.desc()).paginate(page, per_page,
                                                                                                         error_out=False)
        all_events = Event.query.join(Event.users_staff).filter(User.id == id).order_by(
            Event.date_event.desc()).paginate(
            page_event, per_page,
            error_out=False)
        sum_event = len(user.event_staff)
        admin_event = len(user.event)
        if request.method == 'POST':
            if request.files.get('photo'):
                file = request.files['photo']
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                if file and allowed_photo_profile(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(config.Config.UPLOAD_PHOTO_PROFILES, filename))
                    user.photo = filename
                    # form.populate_obj(user)
                    db.session.commit()
                    print('Hello Anrey')
                    return redirect(url_for('profiles.profile', id=user.id))
        return render_template('profile_2.html', menu="team", user=user, events=events, all_events=all_events,
                               sum_event=sum_event,
                               admin_event=admin_event, form=form, send_message=send_message)
    return abort(404)


@profiles.route('/profile/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def profile_edit(id):
    if id == current_user.id:
        per_page = 10
        user = User.query.get(id)
        userss = {'user': user.id}
        form = UserForm(request.form, obj=user, data=userss)

        page = request.args.get('page', type=int, default=1)
        page_event = request.args.get('page_event', type=int, default=1)
        events = Event.query.filter(Event.user_id == user.id).order_by(Event.date_event.desc()).paginate(page, per_page,
                                                                                                         error_out=False)
        all_events = Event.query.join(Event.users_staff).filter(User.id == id).order_by(
            Event.date_event.desc()).paginate(
            page_event, per_page,
            error_out=False)
        sum_event = len(user.event_staff)
        admin_event = len(user.event)
        if request.method == 'POST':
            if user.login != request.form['login']:
                if form.validate():
                    form.populate_obj(user)
                    db.session.commit()
                    return redirect(url_for('main.profile', id=user.id))
                else:
                    return render_template('profile_edit.html', user=user, events=events, all_events=all_events,
                                           sum_event=sum_event,
                                           admin_event=admin_event, form=form)
            else:
                form.populate_obj(user)
                db.session.commit()
                return redirect(url_for('main.profile', id=user.id))
            # return render_template('profile_edit.html', user=user, events=events, all_events=all_events,
            #                        sum_event=sum_event,
            #                        admin_event=admin_event, form=form)

        return render_template('profile_edit.html', user=user, events=events, all_events=all_events,
                               sum_event=sum_event,
                               admin_event=admin_event, form=form)
    return abort(404)


@profiles.route('/managers', methods=['GET'])
@login_required
def managers():
    try:
        managers = User.query.filter(User.roles.any(Role.name.in_(['manager']))).order_by(User.last_name).all()
    except Exception as e:
        logger.warning(
            f'{current_user.last_name} - reads action failed with errors: {e}'
        )
    return render_template('team.html', menu="managers", managers=managers)


@profiles.route('/team', methods=['GET'])
@login_required
def team():
    id = current_user.settings.company_default_id
    if request.args.get('m') == "managers":
        try:
            managers = User.query.filter(User.company_admin.any(Company.id.in_([id]))).filter(
                User.roles.any(Role.name.in_(['manager']))).order_by(User.last_name).all()
        except Exception as e:
            logger.warning(
                f'{current_user.last_name} - reads action failed with errors: {e}'
            )
        return render_template('team.html', menu="team", managers=managers)
    if request.args.get('m') == "admin":
        try:
            managers = User.query.filter(User.company_admin.any(Company.id.in_([id]))).filter(
                User.roles.any(Role.name.in_(['admin']))).order_by(User.last_name).all()
        except Exception as e:
            logger.warning(
                f'{current_user.last_name} - reads action failed with errors: {e}'
            )
        return render_template('team.html', menu="team", managers=managers)
    try:
        # managers = User.query.filter(User.roles.any(Role.name.in_(['user']))).order_by(User.last_name).all()
        managers = User.query.filter(User.company.any(Company.id.in_([id]))).order_by(User.last_name).all()
    except Exception as e:
        logger.warning(
            f'managers - reads action failed with errors: {e}'
        )
    return render_template('team.html', menu="team", managers=managers)


@profiles.route('/admincompanyadd/<int:id>', methods=['GET'])
@login_required
@decorated_admin
def admincompanyadd(id):
    company_id = current_user.settings.company_default_id
    company = Company.query.get(company_id)
    if isinstance(id, int):
        user = User.query.get(id)
        company.admin.append(user)
        db.session.commit()

    return redirect(request.referrer)


@profiles.route('/admincompanyremove/<int:id>', methods=['GET'])
@decorated_admin
def admincompanyremove(id):
    company_id = current_user.settings.company_default_id
    company = Company.query.get(company_id)
    # id = request.args.get('id')
    if isinstance(id, int):
        user = User.query.get(id)
        company.admin.remove(user)
        print(company.admin)
        db.session.commit()

    return redirect(request.referrer)


@profiles.route('/api/send_message/<int:id>', methods=['GET', 'POST'])
@login_required
def send_message(id):
    message = PrivateMessages()
    form = SendMessageForm(request.form, message)
    if request.method == 'POST':
        form.populate_obj(message)
    return redirect(request.referrer)
