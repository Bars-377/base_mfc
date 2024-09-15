from flask_sqlalchemy import SQLAlchemy

# Инициализируем объект SQLAlchemy
db = SQLAlchemy()

class Service(db.Model):
    __tablename__ = 'services'  # Название таблицы в базе данных

    # Определяем поля таблицы
    id = db.Column(db.BigInteger, primary_key=True)  # Поле для уникального идентификатора записи (первичный ключ)
    name = db.Column(db.String(100), nullable=False)  # Название услуги, обязательное поле, максимум 100 символов
    description = db.Column(db.String(200), nullable=False)  # Описание услуги, обязательное поле, максимум 200 символов
    cost = db.Column(db.Float, nullable=False)  # Стоимость услуги, обязательное поле, тип данных - число с плавающей запятой
    year = db.Column(db.Date, nullable=False)  # Год предоставления услуги, обязательное поле, тип данных - дата
    color = db.Column(db.String(7))  # Дополнительное поле для хранения цвета (HEX код), длина 7 символов (включая #), может быть пустым

    # Конструктор класса для создания новых объектов
    def __init__(self, name, description, cost, year, color=None):
        self.name = name  # Устанавливаем название услуги
        self.description = description  # Устанавливаем описание услуги
        self.cost = cost  # Устанавливаем стоимость услуги
        self.year = year  # Устанавливаем год предоставления услуги
        self.color = color  # Устанавливаем цвет (если задан), может быть None (отсутствовать)
