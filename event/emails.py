from event import mail
from flask_mail import Message


def send_msg(email, login):
    msg = Message(f"Hello, {login}",
                  sender=('Администрация TM+', 'support@touremanager.ru'),
                  recipients=[email])
    msg.body = "aaaaaaatesting"
    msg.html = "<b>sssssssssssstesting</b>"
    mail.send(msg)


def send_confirm(email, html):
    msg = Message("Подтверждение email",
                  sender=('Администрация TM+', 'support@touremanager.ru'),
                  recipients=[email])
    # msg.body = html
    msg.html = html
    mail.send(msg)


def send_confirm_succes(email, html):
    msg = Message("Успешное подтверждение",
                  sender=('Администрация TM+', 'support@touremanager.ru'),
                  recipients=[email])
    # msg.body = html
    msg.html = html
    mail.send(msg)


def send_invite(email, html):
    msg = Message("Приглашение",
                  sender=('Администрация TM+', 'support@touremanager.ru'),
                  recipients=[email])
    # msg.body = html
    msg.html = html
    mail.send(msg)


def send_forgot(email, html):
    msg = Message("Востановить пароль",
                  sender="support@touremanager.ru",
                  recipients=[email])
    # msg.body = html
    msg.html = html
    mail.send(msg)
