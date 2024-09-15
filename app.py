# Импортируем необходимые модули из Flask и другие библиотеки
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify  # Импортируем функции для работы с Flask и JSON

from models import db, Service  # Импортируем объекты базы данных и модель Service

# Создаем экземпляр Flask-приложения
app = Flask(__name__)  # Создаем объект Flask, который будет нашим веб-приложением

# Устанавливаем секретный ключ для сессий и флэш-сообщений
app.secret_key = 'supersecretkey'  # Устанавливаем секретный ключ для защиты сессий и флэш-сообщений

# Конфигурируем подключение к базе данных MySQL с использованием SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:enigma1418@localhost/mdtomskbot'  # Указываем строку подключения к базе данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем отслеживание изменений для уменьшения нагрузки на память

# Инициализируем SQLAlchemy с использованием конфигурации Flask
db.init_app(app)  # Инициализируем объект SQLAlchemy с настройками Flask

# Определяем маршрут для главной страницы
@app.route('/')
def index():
    # Получаем параметры запроса
    year = request.args.get('year', None)  # Получаем параметр года из URL (если есть)
    keyword = request.args.get('keyword', None)  # Получаем параметр ключевого слова из URL (если есть)
    page = request.args.get('page', 1, type=int)  # Получаем параметр страницы из URL, по умолчанию 1
    per_page = 20  # Количество записей на странице

    # Получаем все уникальные года для выпадающего списка
    service_years = db.session.query(db.func.year(Service.year)).distinct().all()  # Запрашиваем все уникальные года
    service_years = [str(year[0]) for year in service_years]  # Преобразуем года в строки

    # Фильтрация по году
    query = Service.query  # Начинаем запрос к модели Service
    if year:
        query = query.filter(db.func.year(Service.year) == year)  # Фильтруем по выбранному году

    # Фильтрация по ключевому слову
    if keyword:
        query = query.filter(
            (Service.name.like(f'%{keyword}%')) |
            (Service.description.like(f'%{keyword}%'))
        )  # Фильтруем по ключевому слову в названии и описании

    # Получаем общую сумму для выбранного года
    total_cost_query = query.with_entities(db.func.sum(Service.cost).label('total_cost')).scalar()  # Запрашиваем сумму стоимости
    total_cost = total_cost_query if total_cost_query else 0  # Если сумма отсутствует, устанавливаем 0

    # Пагинация
    offset = (page - 1) * per_page  # Вычисляем смещение для пагинации
    services = query.offset(offset).limit(per_page).all()  # Получаем услуги для текущей страницы
    total_services = query.count()  # Получаем общее количество записей
    total_pages = (total_services + per_page - 1) // per_page  # Вычисляем общее количество страниц

    # Отправляем данные на шаблон для отображения
    return render_template(
        'index.html',
        services=services,
        total_cost=total_cost,
        selected_year=year,
        keyword=keyword,
        page=page,
        total_pages=total_pages,
        service_years=service_years
    )

# Определяем маршрут для страницы редактирования услуги
@app.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    # Получаем услугу по идентификатору или возвращаем ошибку 404, если услуга не найдена
    service = Service.query.get_or_404(id)  # Ищем услугу по ID

    # Отправляем данные на шаблон для редактирования
    return render_template('edit.html', service=service)

from datetime import datetime  # Импортируем datetime для работы с датами

# Определяем маршрут для обновления услуги
@app.route('/edit/<int:id>', methods=['POST'])
def update(id):
    # Пример проверки длины
    name = request.form['name']
    description = request.form['description']
    if len(name) > 20 or len(description) > 20:
        flash('Service Name and Description must be 20 characters or less.')
        return redirect(url_for('index'))

    # Получаем услугу по идентификатору или возвращаем ошибку 404, если услуга не найдена
    service = Service.query.get_or_404(id)

    # Обновляем данные услуги на основе данных из формы
    service.name = request.form['name']
    service.description = request.form['description']
    service.cost = request.form['cost']
    service.year = datetime.strptime(request.form['year'], '%Y-%m-%d').date()  # Преобразуем строку в дату
    service.color = request.form.get('color')  # Получаем значение цвета

    # Сохраняем изменения в базе данных
    db.session.commit()
    flash('Service updated successfully!')  # Отображаем флэш-сообщение об успешном обновлении
    return redirect(url_for('index'))  # Перенаправляем на главную страницу

# Маршрут для обновления цвета
@app.route('/update-color/<int:id>', methods=['POST'])
def update_color(id):
    # Получаем услугу по идентификатору или возвращаем ошибку 404, если услуга не найдена
    service = Service.query.get_or_404(id)

    # Получаем данные из запроса
    data = request.json
    color = data.get('color')  # Получаем цвет из данных запроса

    # Обновляем цвет услуги
    service.color = color
    db.session.commit()  # Сохраняем изменения в базе данных

    # Возвращаем обновленные данные в формате JSON
    return jsonify({
        'success': True,
        'id': service.id,
        'color': service.color,
        'name': service.name,
        'description': service.description,
        'cost': service.cost,
        'year': service.year.strftime('%Y-%m-%d')  # Преобразуем дату в строку
    })

# Определяем маршрут для удаления услуги
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    # Получаем услугу по идентификатору или возвращаем ошибку 404, если услуга не найдена
    service = Service.query.get_or_404(id)

    # Удаляем услугу из базы данных
    db.session.delete(service)
    db.session.commit()  # Сохраняем изменения

    # Показываем флэш-сообщение об успешном удалении
    flash('Service deleted successfully!')

    # Перенаправляем на главную страницу
    return redirect(url_for('index'))

# Определяем маршрут для добавления новой услуги
@app.route('/add', methods=['POST'])
def add():
    # Пример проверки длины
    name = request.form['name']
    description = request.form['description']
    if len(name) > 20 or len(description) > 20:
        flash('Service Name and Description must be 20 characters or less.')
        return redirect(url_for('index'))

    # Получаем данные из формы
    name = request.form['name']
    description = request.form['description']
    cost = request.form['cost']
    year = datetime.strptime(request.form['year'], '%Y-%m-%d').date()  # Преобразуем строку в дату
    color = request.form.get('color')  # Получаем значение цвета

    # Создаем новый объект услуги
    new_service = Service(name=name, description=description, cost=cost, year=year, color=color)
    db.session.add(new_service)  # Добавляем новый объект в базу данных
    db.session.commit()  # Сохраняем изменения
    flash('Service added successfully!')  # Отображаем флэш-сообщение об успешном добавлении
    return redirect(url_for('index'))  # Перенаправляем на главную страницу

import pandas as pd
from io import BytesIO
from flask import send_file
from openpyxl.styles import PatternFill, Border, Side

@app.route('/export-excel', methods=['GET'])
def export_excel():
    year = request.args.get('year', None)

    # Получаем данные для выбранного года
    query = Service.query
    if year and year.isdigit():
        query = query.filter(db.func.year(Service.year) == int(year))

    services = query.all()

    # Создаем DataFrame из данных
    df = pd.DataFrame([{
        'Name': service.name,
        'Description': service.description,
        'Cost': service.cost,
        'Year': service.year.strftime('%Y-%m-%d'),
        'Color': getattr(service, 'color', '')
    } for service in services])

    # Создаем файл Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Services')

        # Настройка стиля
        worksheet = writer.sheets['Services']

        # Определяем стиль для границ
        border_style = Border(left=Side(style='thin'),
                              right=Side(style='thin'),
                              top=Side(style='thin'),
                              bottom=Side(style='thin'))

        # Применяем границы ко всем ячейкам и цвет к ячейкам, где он задан
        for row_num in range(2, worksheet.max_row + 1):  # Пропускаем заголовки
            for col_num in range(1, worksheet.max_column + 1):
                cell = worksheet.cell(row=row_num, column=col_num)
                cell.border = border_style

                # Применяем цвет только к ячейкам данных
                color = df.iloc[row_num - 2]['Color']  # Сопоставление индексов DataFrame
                if color:
                    cell.fill = PatternFill(start_color=color.replace('#', ''), end_color=color.replace('#', ''), fill_type="solid")

        # Применяем границы к заголовкам
        for col_num in range(1, worksheet.max_column + 1):
            cell = worksheet.cell(row=1, column=col_num)
            cell.border = border_style

        # Удаляем столбец Color из Excel-файла
        worksheet.delete_cols(df.columns.get_loc("Color") + 1)

    output.seek(0)

    # Отправляем файл пользователю
    return send_file(output, as_attachment=True, download_name='services.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# Запускаем приложение в режиме отладки
if __name__ == '__main__':
    app.run(debug=True)  # Запускаем сервер Flask с режимом отладки
