from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Инициализируем объект SQLAlchemy
db = SQLAlchemy()

class Service(db.Model):
    __tablename__ = 'services'  # Название таблицы в базе данных

    # Определяем поля таблицы
    id = db.Column(db.BigInteger, primary_key=True)  # Поле для уникального идентификатора записи (первичный ключ)
    id_id = db.Column(db.String(500), nullable=False)
    name = db.Column(db.String(500), nullable=False)  # Название услуги, обязательное поле, максимум 100 символов
    snils = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(500), nullable=False)
    address_p = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    benefit = db.Column(db.String(500), nullable=False)
    number = db.Column(db.String(500), nullable=False)
    year = db.Column(db.String(500), nullable=False)  # Год предоставления услуги, обязательное поле, тип данных - дата
    cost = db.Column(db.String(500), nullable=False)  # Стоимость услуги, обязательное поле, тип данных - число с плавающей запятой
    certificate = db.Column(db.String(500), nullable=False)
    date_number_get = db.Column(db.String(500), nullable=False)
    date_number_cancellation = db.Column(db.String(500), nullable=False)
    date_number_no = db.Column(db.String(500), nullable=False)
    certificate_no = db.Column(db.String(500), nullable=False)
    reason = db.Column(db.String(500), nullable=False)
    track = db.Column(db.String(500), nullable=False)
    date_post = db.Column(db.String(500), nullable=False)  # Год предоставления услуги, обязательное поле, тип данных - дата
    comment = db.Column(db.String(200), nullable=False)  # Описание услуги, обязательное поле, максимум 200 символов
    color = db.Column(db.String(500), nullable=False)  # Дополнительное поле для хранения цвета (HEX код), длина 7 символов (включая #), может быть пустым

    # Конструктор класса для создания новых объектов
    def __init__(self, id_id, name, snils, location,
                address_p, address, benefit, number,
                year, cost, certificate, date_number_get,
                date_number_cancellation, date_number_no,
                certificate_no, reason, track, date_post, comment, id=None, color=None):
        self.id = id
        self.id_id = id_id
        self.name = name  # Устанавливаем название услуги
        self.snils = snils
        self.location = location
        self.address_p = address_p
        self.address = address
        self.benefit = benefit
        self.number = number
        self.year = year  # Устанавливаем год предоставления услуги
        self.cost = cost  # Устанавливаем стоимость услуги
        self.certificate = certificate
        self.date_number_get = date_number_get
        self.date_number_cancellation = date_number_cancellation
        self.date_number_no = date_number_no
        self.certificate_no = certificate_no
        self.reason = reason
        self.track = track
        self.date_post = date_post
        self.comment = comment
        self.color = color  # Устанавливаем цвет (если задан), может быть None (отсутствовать)

from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Явно указываем имя таблицы

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)

    def set_password(self, password):
        """Сохраняем хешированный пароль"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Проверка пароля"""
        return check_password_hash(self.password, password)

    def get_id(self):
        """Возвращает идентификатор пользователя"""
        return str(self.id)

    @property
    def is_active(self):
        """Возвращает True, если пользователь активен"""
        return True

    @property
    def is_authenticated(self):
        """Возвращает True, если пользователь аутентифицирован"""
        return True

    @property
    def is_anonymous(self):
        """Возвращает False, так как анонимный пользователь не поддерживается"""
        return False