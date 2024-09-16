from flask_sqlalchemy import SQLAlchemy

# Инициализируем объект SQLAlchemy
db = SQLAlchemy()

class Service(db.Model):
    __tablename__ = 'services'  # Название таблицы в базе данных

    # Определяем поля таблицы
    id = db.Column(db.BigInteger, primary_key=True)  # Поле для уникального идентификатора записи (первичный ключ)
    name = db.Column(db.String(50), nullable=False)  # Название услуги, обязательное поле, максимум 100 символов
    snils = db.Column(db.BigInteger, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    address_p = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    benefit = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Date, nullable=False)  # Год предоставления услуги, обязательное поле, тип данных - дата
    cost = db.Column(db.Float, nullable=False)  # Стоимость услуги, обязательное поле, тип данных - число с плавающей запятой
    certificate = db.Column(db.Integer, nullable=False)
    date_number_get = db.Column(db.Date, nullable=False)
    date_number_cancellation = db.Column(db.Date, nullable=False)
    date_number_no = db.Column(db.Date, nullable=False)
    certificate_no = db.Column(db.String(50), nullable=False)
    track = db.Column(db.String(50), nullable=False)
    # description = db.Column(db.String(200), nullable=False)  # Описание услуги, обязательное поле, максимум 200 символов
    date_post = db.Column(db.Date, nullable=False)  # Год предоставления услуги, обязательное поле, тип данных - дата
    color = db.Column(db.String(7))  # Дополнительное поле для хранения цвета (HEX код), длина 7 символов (включая #), может быть пустым

    # Конструктор класса для создания новых объектов
    def __init__(self, id,  name, snils, location,
                address_p, address, benefit, number,
                cost, certificate, date_number_get,
                date_number_cancellation, date_number_no,
                certificate_no, track, year, date_post, color=None):
        self.id = id
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
        self.track = track
        # self.description = description  # Устанавливаем описание услуги
        self.date_post = date_post
        self.color = color  # Устанавливаем цвет (если задан), может быть None (отсутствовать)
