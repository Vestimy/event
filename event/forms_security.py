# ----------------------------------------------------
# Program by Andrey Vestimy
#
#
# Version   Date    Info
# 1.0       2020    ----
#
# ----------------------------------------------------
from wtforms import Form, StringField, SelectMultipleField, MultipleFileField, SubmitField, TextAreaField, \
    PasswordField, SelectField, DateField, DateTimeField, IntegerField, validators, TimeField, FileField
from flask_security.forms import RegisterForm, Required, RegisterFormMixin, ValidationError
from event.models import User


class ExtendedRegisterForm(RegisterForm):
    # email = StringField(u'Электронная почта',
    #                     validators=[Required(REQ_TEXT),
    #                                 Length(1, 64),
    #                                 Email(REQ_TEXT)])
    login = StringField('Логин', validators=[])
    first_name = StringField('Имя', [Required()])
    last_name = StringField('Фамилия', [Required()])
    patronymic = StringField('Отчество', [Required()])
    birthday = DateField('Дата рождения')
    phone = StringField('Телефон')
    address = StringField('адрес')

    def validate_login(self, field):
        if User.query.filter_by(login=field.data).first():
            raise ValidationError(u'Login уже занят')

    # birthday = StringField('birthday', [Required()])
