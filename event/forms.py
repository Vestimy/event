import email
from flask_wtf import FlaskForm
from sqlalchemy.orm import eagerload
from wtforms import Form, StringField, SelectMultipleField, MultipleFileField, SubmitField, TextAreaField, \
    PasswordField, SelectField, DateField, DateTimeField, IntegerField, validators, TimeField, FileField, FloatField, \
    BooleanField
from wtforms.validators import DataRequired, Email, InputRequired, ValidationError
from event.models import *
from event.model.city import *
from wtforms.widgets import HiddenInput


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
    # name = StringField("Имя: ")
    artist_id = SelectField("Артист")
    date_event = DateField('Дата', format='%Y-%m-%d')
    typeevent_id = SelectField("Тип")
    # time_event = TimeField("Время мероприятия", format='%H:%M')
    time_event = StringField("Время мероприятия")
    description = StringField("Описание")
    city_id = SelectField("Город")
    arena_id = SelectField("Арена")
    user_id = SelectField("Менеджер")
    users_staffs = SelectMultipleField('Staff')
    submit = SubmitField("Сохранить")

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.typeevent_id.choices = [(g.id, g.name) for g in TypeEvent.query.order_by('name')]
        # self.typeevent_id.choices.insert(0, (0, u"Не выбрана"))

        # self.manager_id.choices = [(g.id, g.name) for g in Manager.query.order_by('name')]
        # self.manager_id.choices.insert(0, (0, u"Не выбрана"))

        self.user_id.choices = [(g.id, g) for g in User.query.filter(User.roles.any(Role.name.in_(["manager"])))]
        self.user_id.choices.insert(0, (None, u"Не выбран"))

        self.artist_id.choices = [(g.id, f'{g.first_name} {g.last_name}') for g in Artist.query.order_by('last_name')]
        self.artist_id.choices.insert(0, (0, u"Не выбран"))
        # self.city_id.choices = \
        # [(g.id, u"%s" % g.name) for g in City.query.order_by('name')]
        #  выбранное поле по умолчанию
        # self.city_id.choices.insert(0, (None, u"Не выбрана"))
        self.city_id.choices = [(0, u"Не выбран")]

        self.users_staffs.choices = [(g.id, g) for g in User.query.all()]
        # self.arena_id.choices = list()
        self.arena_id.choices = [(g.id, g.name) for g in Arena.query.order_by('name')]
        #  выбранное поле по умолчанию
        # self.arena_id.choices.insert(0, (None, u"Не выбрана"))

    def validate_name(self, field):
        event = Event.query.filter(City.name == field.data).first()
        if event:
            raise ValidationError(u'Такой город уже существует')


class CityForm(Form):
    name = StringField('Город', [InputRequired()])
    arena = SelectMultipleField('Арена', validate_choice=False)
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(CityForm, self).__init__(*args, **kwargs)
        # self.arena.choices = [(g.id, g.name) for g in Arena.query.order_by('name') if not g.city_id]

    def validate_name(self, field):
        city = City.query.filter(City.name == field.data).first()
        if city:
            raise ValidationError(u'Такой город уже существует')


class CitysForm(Form):
    name = SelectField('Город', [InputRequired()])
    arena = SelectMultipleField('Арена', validate_choice=False)
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(CitysForm, self).__init__(*args, **kwargs)
        # self.arena.choices = [(g.id, g.name) for g in Arena.query.order_by('name') if not g.city_id]
        # self.name.choices = [(g.id, g.name) for g in City.query.order_by('name')]
        q = Region.query.filter(Region.country_id == 1).order_by('name').all()
        print(q)
        self.name.choices = [(i.id, i.name) for g in q for i in g.city]

    # def validate_name(self, field):
    #     city = City.query.filter(City.name == field.data).first()
    #     if city:
    #         raise ValidationError(u'Такой город уже существует')


class ArenaForm(Form):
    name = StringField('Название')
    alias = StringField('Сокращенное название')
    description = StringField('Описание')
    city_id = SelectField('Город', validate_choice=False)
    typehall_id = SelectField('Тип площадки', validate_choice=False)
    address = StringField('Адрес')
    email = StringField('email')
    url = StringField('Сайт')
    phone_admin = StringField('Тел. Администратора')
    number_of_seats = StringField('Количество мест')
    hall_size = StringField('Размеры зала')
    razgruzka = StringField('Разгрузка')
    sound = StringField('Местный звук')
    phone_sound = StringField('Тел. Звукорежиссера')
    light = StringField('Местный свет')
    phone_light = StringField('Тел. Свет')

    img = FileField("Фото")
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(ArenaForm, self).__init__(*args, **kwargs)
        # self.city_id.choices = [(g.id, g.name) for g in City.query.order_by('name')]
        self.typehall_id.choices = [(g.id, g.name) for g in TypeHall.query.order_by('name')]

    def validate_name(self, field):
        arena = Arena.query.filter(Arena.name == field.data).first()
        if arena:
            raise ValidationError(u'Площадка уже существует')


class ArtistForm(Form):
    last_name = StringField('Фамилия')
    first_name = StringField('Имя')
    alias = StringField('Псевдоним')
    description = TextAreaField('Описание')
    administrator = StringField('Администратор')
    email_admin = StringField('Почта')
    phone_administrator = StringField('Тел. ')
    sound_engineer = StringField('Звукорежиссер')
    email_sound = StringField('Почта')
    phone_sound = StringField('Тел.')
    monitor_engineer = StringField('Мон. Звукорежиссер')
    email_monitor = StringField('Почта')
    phone_monitor = StringField('Тел.')
    light = StringField('Художник по свету')
    email_light = StringField('Почта ')
    phone_light = StringField('Тел. ')
    img = FileField("Фото")

    submit = SubmitField('Сохранить')

    def validate_name(self, field):
        artist = Artist.query.filter(Artist.name == field.data).first()
        if artist:
            raise ValidationError('Такой артист уже существует')


class ManagerForm(Form):
    last_name = StringField('Фамилия')
    first_name = StringField('Имя')
    patronymic = StringField('Отчество')
    phone = StringField('Телефон')
    address = StringField('Адрес')
    birthday = DateField('День рождения')
    facebook = StringField('Facebook')
    instagram = StringField('Instagram')
    photo = FileField("Фото")
    document_id = MultipleFileField("Документы")
    submit = SubmitField('Сохранить')


# class EmailString(StringField):
#     def pre_validate(self, form):
#
#         print(form.email.data)
#         if User.query.filter(User.email == form.email.data).first():
#             raise ValueError("EWFWEW")


class UserForm(Form):
    id = Integer
    last_name = StringField('Фамилия')
    first_name = StringField('Имя')
    patronymic = StringField('Отчество')
    login = StringField('Логин')
    email = StringField('Почта')
    phone = StringField('Телефон')
    address = StringField('Адрес')
    birthday = DateField('День рождения')
    facebook = StringField('Facebook')
    instagram = StringField('Instagram')
    photo = FileField("Фото")
    document_id = MultipleFileField("Документы")
    submit = SubmitField('Сохранить')

    def validate_login(self, field):
        if User.query.filter(User.login == field.data).first():
            raise ValidationError('Пользователь с таким логином уже существует')


class ProfileImg(Form):
    photo = FileField('Фотография')

    submit = SubmitField('Сохранить')
    # def validate_login(self, field):
    #     if User.query.filter(User.login == field.data).first():
    #         raise ValidationError('Пользователь с таким логином уже существует')


# class RegisterForm(Form):
#     name = StringField('Имя')
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Парлоь')
#     submit = SubmitField('Зарегестрироваться')


class UploadForm(Form):
    file = FileField('Выбирите изображение')
    save = SubmitField('Сохранить')


class TestForm(Form):
    x = FloatField(widget=HiddenInput())
    y = FloatField(widget=HiddenInput())
    width = FloatField(widget=HiddenInput())
    height = FloatField(widget=HiddenInput())


class LoginForm(Form):
    email = StringField('Email или Логин', [validators.Length(min=6, max=35)])
    password = PasswordField('Пароль', [
        validators.Required(),
    ])
    remember = BooleanField('Remember me', default=False)
    submit = SubmitField('Войти')

    def validate_on_submit(self):
        pass


class ForgotPasswordForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=35)])
    submit = SubmitField('Восстановить')

    def validate_email(self, feald):
        user = User.query.filter(User.email == feald.data).first()
        if user is None:
            raise ValidationError('Такой email не зарегистрирован')


class RegisterUserForm(Form):
    email = StringField('Email', [validators.Length(min=4, max=35)])
    login = StringField(' Логин')
    password = PasswordField('Пароль', [
        validators.Required(), validators.Length(min=6, max=35, message="Пароль меньше 6 символов")
    ])
    password_confirm = PasswordField('Пароль', [
        validators.Required(),
        validators.Length(min=6, max=35, message="Пароль меньше 6 символов")
    ])
    last_name = StringField('Фамилия')
    first_name = StringField('Имя')
    # patronymic = StringField('Отчество')

    birthday = DateField('День рождения')
    phone = StringField('Телефон')
    address = StringField('Адрес')

    submit = SubmitField('Регистрация')

    def validate_email(self, feald):
        user = User.query.filter(User.email == feald.data).first()
        if user:
            raise ValidationError('Email занят')

    def validate_login(self, feald):
        if User.query.filter(User.login == feald.data).first():
            raise ValidationError('Логин занят')


class CompanyForm(Form):
    name = StringField('Название', [validators.Length(min=4, max=35)])
    email = StringField(' Email')

    phone = StringField('Телефон')
    address = StringField('Адрес')
    # patronymic = StringField('Отчество')

    instagram = StringField('Инстраграм')
    vk = StringField('Телефон')
    facebook = StringField('Адрес')

    city_id = SelectField('Город')
    companytype_id = SelectField('Компания')

    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.companytype_id.choices = [(i.id, i.name) for i in CompanyType.query.all()]

    def validate_name(self, feald):
        company = Company.query.filter(Company.name == feald.data).first()
        if company:
            raise ValidationError('Email занят')


class InviteForm(Form):
    email = StringField('Email')
    submit = SubmitField('Пригласить')

    def validate_email(self, feald):
        email = Invite.query.filter(Invite.email == feald.data).first()
        if email:
            raise ValidationError('Пришлашение выслано')