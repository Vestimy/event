from flask import Blueprint, jsonify, request, render_template, redirect
from event import logger, config
from werkzeug.utils import secure_filename
import uuid
from event import logger, config
from event.models import *
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from blog.base_view import BaseView
# from blog.utils import upload_file

from flask_security import login_required, roles_required, current_user, login_user, roles_accepted
import os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from event.forms import *

managers = Blueprint('managers', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

UPLOAD_FOLDER = 'static'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@managers.route('/manager/', methods=['GET'])
@login_required
def get_list_manager():
    try:
        # manager = Manager.query.order_by('name').all()

        manager = User.query.filter(User.roles.any(Role.name.in_(['manager']))).all()
    except Exception as e:
        logger.warning(
            f'managers - reads action failed with errors: {e}'
        )
    return render_template('manager/get_manager.html', menu='managers', managers=manager)


@managers.route('/manager/<int:id>', methods=['GET'])
@login_required
def get_item_manager(id):
    try:
        # manager = Manager.query.get(id)
        # manager = User.query.filter.any(Role.name.in_('manager'))
        manager = User.query.get(id)
        event = Event.query.filter(Event.user_id == manager.id).order_by(Event.date_event.desc()).all()
        # event = Non
    except Exception as e:
        logger.warning(
            f'managers - read action failed with errors: {e}'
        )
    return render_template('manager/item_manager.html', menu='managers', event=event, item=manager)


@managers.route('/manager/add', methods=['GET', 'POST'])
@login_required
def add_manager():
    form = ManagerForm()
    # form.city_id.choices = ArenaForm.city_choices()
    # form.city_id.choices = [(g.id, g.name) for g in City.query.order_by('name')]
    if request.method == 'POST':

        # print(request.form)
        manager = Manager(name=request.form['name'],
                          phone=request.form['phone']
                          )

        try:
            db.session.add(manager)
            db.session.commit()

        except Exception as e:
            logger.warning(
                f'managers - wright action failed with errors: {e}'
            )
            db.session.rollback()
        return redirect(url_for('managers.get_list_manager'))

    return render_template('manager/add_manager.html', menu='managers', form=form)


@managers.route('/manager/delete/<int:id>', methods=['GET'])
@login_required
def delete_manager(id):
    try:
        manager = User.query.get(id)
        role = Role.query.filter(Role.name == "manager").one()
        manager.roles.remove(role)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.warning(
            f"{current_user.name} - Ошибка при удалении менеджера: {e}"
        )
    return redirect(url_for('managers.get_list_manager'))


@managers.route('/manager/edit/<int:id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'manager')
def edit_manager(id):
    # manager = Manager.query.get(id)
    manager = User.query.get(id)
    form = ManagerForm(request.form, obj=manager)
    if current_user.has_role('admin') or current_user.id == manager.id:
        if request.method == 'POST':
            if request.files['photo']:
                file = request.files['photo']
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                try:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join('/home/vestimy/project/python/event/event/static/profiles', filename))
                        form.populate_obj(manager)
                        manager.photo = "profiles/" + filename
                        db.session.commit()
                        return render_template('manager/edit_manager.html', menu='managers', item=manager, form=form)
                except Exception as e:
                    db.session.rollback()
                    logger.warning(
                        f"{current_user.name} - Ошибка при обновлении профиля: {e}"
                    )

            form.populate_obj(manager)
            db.session.commit()
            return redirect(url_for('managers.get_list_manager'))

        # form.city_id.choices = [(g.id, g.name) for g in City.query.order_by('name')]
        return render_template('manager/edit_manager.html', menu='managers', item=manager, form=form)
    return redirect(url_for("main.index"))

@managers.route('/arena/img_add', methods=['GET', 'POST'])
@login_required
def arena_img_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            item = ImgArena(url=filename)
            db.session.add(item)
            db.session.commit()
            file.save(os.path.join('/home/vestimy/project/python/event/event/static', filename))
            return redirect(url_for('arenas.arena_img_upload',
                                    filename=filename))

    else:
        return render_template('upload.html', menu='arenas')


@managers.route('/manager/add', methods=['POST'])
@login_required
def add_photo_manager():
    form = request.form
    print(form)


@managers.route('/manager/img_add', methods=['GET', 'POST'])
@login_required
def manager_img_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        try:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = str(uuid.uuid4())


                print(filename)

                item = ManagerPhoto(url="managers/"+filename)
                db.session.add(item)
                db.session.commit()
                file.save(os.path.join('/home/vestimy/project/python/event/event/static/managers', filename))
                return redirect(url_for('managers.manager_img_upload', filename=filename))
        except Exception as e:
            db.session.rollback()

    else:
        return render_template('upload.html', menu='arenas')


@managers.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400
