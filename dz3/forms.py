from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


class RegistrationForm(FlaskForm):
    username = StringField('Введите имя пользователя')
    usersurname = StringField('Введите фамилию пользователя')
    email = StringField('Введите адрес эл. почты', validators=[DataRequired(), Email()])
    password = PasswordField('Введите пароль', validators=[DataRequired(), Length(min=8),
                                         Regexp('(?=.*[a-z])(?=.*[0-9])', message="Ошибка! Нужны цифры и буквы!")])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])

