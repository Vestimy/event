from flask import Blueprint, jsonify, request, json, render_template, redirect
from flask import abort
from event import logger, config, generate_id
from event.emails import send_invite
from werkzeug.utils import secure_filename
from event import logger, config, allowed_photo_profile
# from blog.schemas import VideoSchema, UserSchema, AuthSchema
# from flask_apispec import use_kwargs, marshal_with
from event.models import *
from event.model.security import *
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from blog.base_view import BaseView
# from blog.utils import upload_file
import os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_security import login_required, current_user
from event.decorators import decorated_admin
from event.forms import *

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
@login_required
def mains():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))


@main.route('/index', methods=['GET'])
@login_required
def index():
    # title = Company.query.get(current_user.settings.company_default_id)
    last_event = Event.query[-1]
    return render_template('index.html', menu='index', last_event=last_event)


@main.route('/profile/', methods=['GET'])
@login_required
def profile_all():
    if current_user.is_authenticated:
        id = current_user.id
        user = User.query.get(id)
        return redirect(url_for('main.profile', id=id))
    return redirect(url_for('security.login'))


@main.route('/profile/<int:id>', methods=['GET', "POST"])
@login_required
def profile(id, page=1):
    per_page = 10
    user = User.query.get(id)
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
                    return redirect(url_for('main.profile', id=user.id))
        return render_template('profile.html', menu="team", user=user, events=events, all_events=all_events,
                               sum_event=sum_event,
                               admin_event=admin_event, form=form)
    return abort(404)


@main.route('/profile/edit/<int:id>', methods=['GET', 'POST'])
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


@main.route('/managers', methods=['GET'])
@login_required
def managers():
    try:
        managers = User.query.filter(User.roles.any(Role.name.in_(['manager']))).order_by(User.last_name).all()
    except Exception as e:
        logger.warning(
            f'{current_user.last_name} - reads action failed with errors: {e}'
        )
    return render_template('team.html', menu="managers", managers=managers)


@main.route('/team', methods=['GET'])
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


@main.route('/invite', methods=['GET', 'POST'])
@login_required
def invite():
    default_id = current_user.settings.company_default_id
    company = Company.query.get(default_id)
    """"""
    if current_user.creator or current_user in company.user_admin:
        if request.args.get('delete'):
            db.session.delete(Invite.query.get(request.args.get('delete')))
            db.session.commit()
            return redirect(url_for('main.invite'))
        invite = Invite.query.filter(Invite.company_id == default_id)
        inv = Invite()
        form = InviteForm(request.form, obj=inv)

        if request.method == 'POST' and form.validate():
            invite_id = generate_id()
            company_id = company.id
            form.populate_obj(inv)
            inv.invite_id = invite_id
            inv.company_id = company_id
            db.session.add(inv)
            db.session.commit()
            html = render_template('email_templates/action_invite.html', email=inv.email, id=invite_id)
            send_invite(inv.email, html)

            return redirect(url_for('main.invite'))

        return render_template('invite.html', invite=invite, form=form)
    return redirect(url_for('main.index'))


@main.route('/city', methods=['GET', 'POST'])
def city():
    form = CitysForm()
    try:
        city = City()
    except Exception as e:
        logger.warning(
            f'managers - reads action failed with errors: {e}'
        )
    return render_template('form_basic.html', form=form)


@main.route('/calendar', methods=['GET'])
def calendar():
    return render_template('main/cal.html', menu='calendars')


@main.route('/get_calendar', methods=['GET', 'POST'])
# @login_required
def get_calendar():
    event = Event.query.all()
    list_json = []
    for item in event:
        title = f'{item.artist.last_name}'
        start = item.date_event.strftime("%Y-%m-%d")
        if item.artist.first_name:
            title = f'{item.artist.last_name} {item.artist.first_name}'
        if item.time_event:
            start = item.date_event.strftime("%Y-%m-%d") + "T" + item.time_event.strftime("%H:%M:%S")
        list_json.append({
            "title": title,
            "start": start,
            "description": item.description,
            "url": url_for("events.get_item_event", id=item.id)
        })

    return json.dumps(list_json)


@main.route('/default_company/<int:id>', methods=['GET', 'POST'])
@login_required
def default_company(id):
    user = User.query.get(current_user.id)
    if user:
        settings = Settings.query.get(user.settings_id)
        if settings:
            settings.company_default_id = id
            db.session.commit()
            return redirect(request.referrer)


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


@main.route('/admincompanyadd/<int:id>', methods=['GET'])
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

@main.route('/admincompanyremove/<int:id>', methods=['GET'])
@login_required
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
# docs.register(get_list, blueprint='videos')
# docs.register(update_list, blueprint='videos')
# docs.register(update_tutorial, blueprint='videos')
# docs.register(delete_list, blueprint='videos')
# # docs.register(get_video, blueprint=videos)
# ListView.register(videos, docs, '/main', 'listview')
