from flask_wtf import FlaskForm
from wtforms import Form, StringField, SelectMultipleField, MultipleFileField, SubmitField, TextAreaField, \
    PasswordField, SelectField, DateField, DateTimeField, IntegerField, validators, TimeField, FileField
from wtforms.validators import DataRequired, Email, InputRequired, ValidationError
from event.models import *
from flask_admin.form import widgets
from flask_admin.form.widgets import DateTimePickerWidget
from flask_security.forms import RegisterForm, Required, RegisterFormMixin, ValidationError


class LoginForm(Form):
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Submit')


class ContactForm(Form):
    name = StringField("Name: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[Email()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit")


class TourForm(Form):
    name = StringField("Название тура: ")
    # event = SelectMultipleField('Мероприятия')
    event_id = SelectMultipleField('Мероприятия')
    submit = SubmitField("Сохранить")

    def __init__(self, *args, **kwargs):
        super(TourForm, self).__init__(*args, **kwargs)
        self.event_id.choices = [(g.id, g) for g in Event.query.order_by('date_event') if g.tour is None]


class EventForm(Form):
    name = StringField("Имя: ")
    artist_id = SelectField("Артист")
    # date_event = DateField('Дата', format='%Y.%m.%d',
    #                          render_kw={'placeholder': '2020.10.22 for June 20, 2015'})
    date_event = DateField('Дата', format='%Y-%m-%d')
    #
    # datepicker = DateTimeField('Start at')
    typeevent_id = SelectField("Тип")
    time_event = TimeField("Время мероприятия", format='%H:%M')
    description = StringField("Описание")
    city_id = SelectField("Город")
    arena_id = SelectField("Арена")
    user_id = SelectField("Менеджер")

    submit = SubmitField("Сохранить")

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.typeevent_id.choices = [(g.id, g.name) for g in TypeEvent.query.order_by('name')]
        self.typeevent_id.choices.insert(0, (0, u"Не выбрана"))

        # self.manager_id.choices = [(g.id, g.name) for g in Manager.query.order_by('name')]
        # self.manager_id.choices.insert(0, (0, u"Не выбрана"))

        self.user_id.choices = [(g.id, g.name) for g in User.query.filter(User.roles.any(Role.name.in_(["manager"])))]
        self.user_id.choices.insert(0, (0, u"Не выбрана"))

        self.artist_id.choices = [(g.id, g.name) for g in Artist.query.order_by('name')]
        self.artist_id.choices.insert(0, (0, u"Не выбран"))
        self.city_id.choices = \
            [(g.id, u"%s" % g.name) for g in City.query.order_by('name')]
        #  выбранное поле по умолчанию
        self.city_id.choices.insert(0, (0, u"Не выбрана"))

        # self.arena_id.choices = list()
        self.arena_id.choices = [(g.id, u"%s" % g.name) for g in Arena.query.order_by('name')]
        #  выбранное поле по умолчанию
        self.arena_id.choices.insert(0, (0, u"Не выбрана"))


class CityForm(Form):
    name = StringField('Город')
    arena = SelectMultipleField('Арена', validate_choice=False)
    submit = SubmitField('Сохранить')


class ArenaForm(Form):
    name = StringField('Название')
    description = StringField('Описание')
    city_id = SelectField('Город', validate_choice=False)
    typehall_id = SelectField('Тип площадки', validate_choice=False)
    address = StringField('Адрес')
    phone_admin = StringField('Тел. Администратора')
    number_of_seats = IntegerField('Количество мест')
    hall_size = StringField('Размеры зала')
    razgruzka = StringField('Разгрузка')
    sound = StringField('Местный звук')
    phone_sound = StringField('Тел. Звукорежиссера')
    light = StringField('Местный свет')
    phone_light = StringField('Тел. Свет')

    submit = SubmitField('Сохранить')

    # @classmethod
    # def city_choices(cls):
    #     return [(g.id, g.name) for g in City.query.order_by('name')]
    # @classmethod
    # def typehall_choices(cls):
    #     return [(g.id, g.name) for g in TypeHall.query.order_by('name')]

    def __init__(self, *args, **kwargs):
        super(ArenaForm, self).__init__(*args, **kwargs)
        self.city_id.choices = [(g.id, g.name) for g in City.query.order_by('name')]
        self.city_id.choices.insert(0, (0, u"Не выбран"))

        self.typehall_id.choices = [(g.id, g.name) for g in TypeHall.query.order_by('name')]
        self.typehall_id.choices.insert(0, (0, u"Не выбран"))
        # self.city_id.choices = \
        #     [(g.id, u"%s" % g.name) for g in City.query.order_by('name')]
        # #  выбранное поле по умолчанию
        # self.city_id.choices.insert(0, (0, u"Не выбрана"))
        #
        # # self.arena_id.choices = list()
        # self.arena_id.choices = [(g.id, u"%s" % g.name) for g in Arena.query.order_by('name')]
        # #  выбранное поле по умолчанию
        # self.arena_id.choices.insert(0, (0, u"Не выбрана"))


class ArtistForm(Form):
    name = StringField('Артист', validators=[])
    administrator = StringField('Администратор')
    phone_administrator = StringField('Тел. Администратора')
    sound_engineer = StringField('Звукорежиссер')
    phone_sound = StringField('Тел. Звукорежиссера')
    monitor_engineer = StringField('Мон. Звукорежиссер')
    phone_monitor = StringField('Тел. Мон. Звукорежиссера')
    light = StringField('Световик')
    phone_light = IntegerField('Тел. Световика')

    submit = SubmitField('Сохранить')

    def validate_name(self, field):
        print("Попадает сюда")
        if Artist.query.filter(name=field.data).first():
            print("lsfkelwkfewlfkewlfk;welkf")
            raise ValidationError(u'Login уже занят')


class ManagerForm(Form):
    name = StringField('ФИО')
    phone = StringField('Телефон')
    address = StringField('Адрес')
    birthday = DateField('День рождения')
    facebook = StringField('Facebook')
    instagram = StringField('Instagram')

    submit = SubmitField('Сохранить')


# class RegisterForm(Form):
#     name = StringField('Имя')
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Парлоь')
#     submit = SubmitField('Зарегестрироваться')


class UploadForm(Form):
    file = FileField('Выбирите изображение')
    save = SubmitField('Сохранить')


class ExtendedRegisterForm(RegisterForm):
    # email = StringField(u'Электронная почта',
    #                     validators=[Required(REQ_TEXT),
    #                                 Length(1, 64),
    #                                 Email(REQ_TEXT)])
    login = StringField('Логин', validators=[])
    name = StringField('Имя', [Required()])
    last_name = StringField('Фамилия', [Required()])
    birthday = DateField('Дата рождения')
    phone = StringField('Телефон')
    address = StringField('адрес')

    def validate_login(self, field):
        if User.query.filter_by(login=field.data).first():
            raise ValidationError(u'Login уже занят')

    # birthday = StringField('birthday', [Required()])
