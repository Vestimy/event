from flask import Blueprint, render_template, redirect, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from blog.base_view import BaseView
from flask_apispec import use_kwargs, marshal_with
from blog import logger, docs, session
from blog.schemas import UserSchema, AuthSchema
from blog.models import Admin, User
from blog.forms import LoginForm, ContactForm

logins = Blueprint('logins', __name__)


@logins.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flash('Logged in successfully.')

        next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return redirect(next or flask.url_for('index'))
    return render_template('login.html', form=form)


# AdminAuthView.register(admin, docs, '/admin', 'adminauthview')
# AdminUsersView.register(admin, docs, '/admin', 'adminuserview')