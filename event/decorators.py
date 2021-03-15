# ----------------------------------------------------
# Program by Andrey Vestimy
#
#
# Version   Date    Info
# 1.0       2020    ----
#
# ----------------------------------------------------
from flask_login import current_user, login_required
from flask import redirect, url_for, flash
from functools import wraps


def admin_required(func):
    """
    Modified login_required decorator to restrict access to admin group.
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_anonymous:
            if not 'admin' in current_user.roles:  # zero means admin, one and up are other groups
                flash("You don't have permission to access this resource.", "warning")
                return redirect(url_for("main.index"))
        return func(*args, **kwargs)

    return decorated_view


def admin_company(func):
    """
    Modified login_required decorator to restrict access to admin group.
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_anonymous:
            if not 'admin' in current_user.roles:  # zero means admin, one and up are other groups
                flash("You don't have permission to access this resource.", "warning")
                return redirect(url_for("main.index"))
        return func(*args, **kwargs)

    return decorated_view


def decorated_login(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_anonymous:
            if not 'admin' in current_user.roles:  # zero means admin, one and up are other groups
                flash("You don't have permission to access this resource.", "warning")
                return redirect(url_for("main.index"))
        return func(*args, **kwargs)

    return decorated_view
