from flask_wtf import FlaskForm
from wtforms import Form, StringField, SelectMultipleField, MultipleFileField, SubmitField, TextAreaField, \
    PasswordField, SelectField, DateField, DateTimeField, IntegerField, validators, TimeField, FileField
from wtforms.validators import DataRequired, Email, InputRequired, ValidationError
from event.models import *


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
    date_event = DateField('Дата', format='%Y-%m-%d')
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
        # self.typeevent_id.choices.insert(0, (0, u"Не выбрана"))

        # self.manager_id.choices = [(g.id, g.name) for g in Manager.query.order_by('name')]
        # self.manager_id.choices.insert(0, (0, u"Не выбрана"))

        self.user_id.choices = [(g.id, g) for g in User.query.filter(User.roles.any(Role.name.in_(["manager"])))]
        self.user_id.choices.insert(0, (None, u"Не выбран"))

        self.artist_id.choices = [(g.id, f'{g.last_name} {g.first_name}') for g in Artist.query.order_by('last_name')]
        self.artist_id.choices.insert(0, (0, u"Не выбран"))
        self.city_id.choices = \
            [(g.id, u"%s" % g.name) for g in City.query.order_by('name')]
        #  выбранное поле по умолчанию
        self.city_id.choices.insert(0, (None, u"Не выбрана"))

        # self.arena_id.choices = list()
        self.arena_id.choices = [(g.id, g.name) for g in Arena.query.order_by('name')]
        #  выбранное поле по умолчанию
        self.arena_id.choices.insert(0, (0, u"Не выбрана"))

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
        self.arena.choices = [(g.id, g.name) for g in Arena.query.order_by('name') if not g.city_id]

    def validate_name(self, field):
        city = City.query.filter(City.name == field.data).first()
        if city:
            raise ValidationError(u'Такой город уже существует')


class ArenaForm(Form):
    name = StringField('Название')
    description = StringField('Описание')
    city_id = SelectField('Город', validate_choice=False)
    typehall_id = SelectField('Тип площадки', validate_choice=False)
    address = StringField('Адрес')
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
        self.city_id.choices = [(g.id, g.name) for g in City.query.order_by('name')]
        self.typehall_id.choices = [(g.id, g.name) for g in TypeHall.query.order_by('name')]

    def validate_name(self, field):
        arena = Arena.query.filter(Arena.name == field.data).first()
        if arena:
            raise ValidationError(u'Площадка уже существует')


class ArtistForm(Form):
    last_name = StringField('Фамилия')
    first_name = StringField('Имя')
    administrator = StringField('Администратор')
    phone_administrator = StringField('Тел. Администратора')
    sound_engineer = StringField('Звукорежиссер')
    phone_sound = StringField('Тел.')
    monitor_engineer = StringField('Мон. Звукорежиссер')
    phone_monitor = StringField('Тел.')
    light = StringField('Художник по свету')
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


# class RegisterForm(Form):
#     name = StringField('Имя')
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Парлоь')
#     submit = SubmitField('Зарегестрироваться')


class UploadForm(Form):
    file = FileField('Выбирите изображение')
    save = SubmitField('Сохранить')
