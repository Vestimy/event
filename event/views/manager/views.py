import os
from flask import Blueprint, jsonify, request, render_template, redirect
from event import logger, config, allowed_photo_profile, allowed_document_profile

from flask_security import login_required, roles_required, current_user, login_user, roles_accepted
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from event.forms import *

managers = Blueprint('managers', __name__)

ALLOWED_PHOTO = set(['png', 'jpg', 'jpeg', 'gif'])

UPLOAD_FOLDER = 'static'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@managers.route('/manager/', methods=['GET'])
@login_required
def get_list_manager():
    try:
        manager = User.query.filter(User.roles.any(Role.name.in_(['manager']))).order_by(User.last_name).all()
    except Exception as e:
        logger.warning(
            f'managers - reads action failed with errors: {e}'
        )
    return render_template('manager/get_manager.html', menu='managers', managers=manager)


@managers.route('/manager/<int:id>', methods=['GET'])
@login_required
def get_item_manager(id):
    try:
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
    if request.method == 'POST':
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


# @managers.route('/manager/edit/<int:id>', methods=['GET', 'POST'])
# @roles_accepted('admin', 'manager')
# def edit_manager(id):
#     # manager = Manager.query.get(id)
#     manager = User.query.get(id)
#     form = ManagerForm(request.form, obj=manager)
#     if current_user.has_role('admin') or current_user.id == manager.id:
#         if request.method == 'POST':
#             if request.files['photo']:
#                 file = request.files['photo']
#                 if file.filename == '':
#                     flash('No selected file')
#                     return redirect(request.url)
#                 try:
#                     if file and allowed_photo_profile(file.filename):
#                         filename = secure_filename(file.filename)
#                         file.save(os.path.join(config.Config.UPLOAD_PHOTO_PROFILES, filename))
#                         form.populate_obj(manager)
#                         manager.photo = filename
#                         db.session.commit()
#                         return render_template('manager/edit_manager.html', menu='managers', item=manager, form=form)
#                 except Exception as e:
#                     db.session.rollback()
#                     logger.warning(
#                         f"{current_user.first_name} - Ошибка при обновлении профиля: {e}"
#                     )
#                     return redirect(request.url)
#             form.populate_obj(manager)
#             db.session.commit()
#             return redirect(url_for('managers.get_list_manager'))
#
#         return render_template('manager/edit_manager.html', menu='managers', item=manager, form=form)
#     return redirect(url_for("main.index"))

@managers.route('/manager/edit/<int:id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'manager')
def edit_manager(id):
    # manager = Manager.query.get(id)
    manager = User.query.get(id)
    document_load = Document.query.filter(Document.users_id == manager.id).all()
    form = ManagerForm(request.form, obj=manager)
    if current_user.has_role('admin') or current_user.id == manager.id:
        form.populate_obj(manager)
        if request.files.get('photo'):
        # if request.files['photo']:
            file = request.files['photo']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_photo_profile(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(config.Config.UPLOAD_PHOTO_PROFILES, filename))
                manager.photo = filename
        if request.files.get('document_id'):
            # return redirect(request.url)
            files = request.files.getlist('document_id')
            documents = []
            for i in files:
                if allowed_document_profile(i.filename):
                    if i.filename != '':
                        docname = secure_filename(i.filename)
                        i.save(os.path.join(config.Config.UPLOAD_DOCUMENTS_PROFILES, docname))
                        documents.append(Document(name=docname))
            # print("KEWJLKFJ")
            db.session.add_all(documents)
            db.session.commit()
            for i in documents:
                manager.document.append(i)
            db.session.commit()

            # files = request.files.getlist('document_id')
            # for i in files:
            #     dic[i.filename] = i.read()
            # print(files)
            # print(dic)
        return render_template('manager/edit_manager.html', menu='managers', item=manager, form=form, documents=document_load)
    # return redirect(url_for("main.index"))




@managers.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400
