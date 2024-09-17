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
    print('NEVEROV', year)
    keyword = request.args.get('keyword', None)  # Получаем параметр ключевого слова из URL (если есть)
    page = request.args.get('page', 1, type=int)  # Получаем параметр страницы из URL, по умолчанию 1
    per_page = 20  # Количество записей на странице

    # Получаем все уникальные года для выпадающего списка
    service_years = db.session.query(db.func.year(Service.year)).distinct().all()  # Запрашиваем все уникальные года
    service_years = [str(year[0]) for year in service_years]  # Преобразуем года в строки

    # Фильтрация по году
    query = Service.query  # Начинаем запрос к модели Service
    if year:
        if year == 'None':
            year = None
            query = query.filter(db.func.year(Service.year) == year)  # Фильтруем по выбранному году
            year = 'None'
        else:
            query = query.filter(db.func.year(Service.year) == year)  # Фильтруем по выбранному году

    # Фильтрация по ключевому слову
    if keyword:
        query = query.filter(
            (Service.name.like(f'%{keyword}%')) |
            (Service.snils.like(f'%{keyword}%')) |
            (Service.location.like(f'%{keyword}%')) |
            (Service.address_p.like(f'%{keyword}%')) |
            (Service.address.like(f'%{keyword}%')) |
            (Service.benefit.like(f'%{keyword}%')) |
            (Service.number.like(f'%{keyword}%')) |
            (Service.year.like(f'%{keyword}%')) |
            (Service.cost.like(f'%{keyword}%')) |
            (Service.certificate.like(f'%{keyword}%')) |
            (Service.date_number_get.like(f'%{keyword}%')) |
            (Service.date_number_cancellation.like(f'%{keyword}%')) |
            (Service.date_number_no.like(f'%{keyword}%')) |
            (Service.certificate_no.like(f'%{keyword}%')) |
            (Service.reason.like(f'%{keyword}%')) |
            (Service.track.like(f'%{keyword}%')) |
            (Service.date_post.like(f'%{keyword}%'))
        )  # Фильтруем по ключевому слову в названии и описании

    # Сортировка по возрастанию года
    query = query.order_by(Service.year.asc())

    # Получаем общую сумму для выбранного года
    total_cost_query = query.with_entities(db.func.sum(Service.cost).label('total_cost')).scalar()  # Запрашиваем сумму стоимости
    total_cost_1 = total_cost_query if total_cost_query else 0  # Если сумма отсутствует, устанавливаем 0

    # Получаем общую сумму для выбранного года
    total_cost_query = query.with_entities(db.func.sum(Service.certificate).label('total_cost')).scalar()  # Запрашиваем сумму стоимости
    total_cost_2 = total_cost_query if total_cost_query else 0  # Если сумма отсутствует, устанавливаем 0

    # Получаем общую сумму для выбранного года
    total_cost_query = query.with_entities(db.func.sum(Service.certificate_no).label('total_cost')).scalar()  # Запрашиваем сумму стоимости
    total_cost_3 = total_cost_query if total_cost_query else 0  # Если сумма отсутствует, устанавливаем 0

    # Пагинация
    offset = (page - 1) * per_page  # Вычисляем смещение для пагинации
    services = query.offset(offset).limit(per_page).all()  # Получаем услуги для текущей страницы
    total_services = query.count()  # Получаем общее количество записей
    total_pages = (total_services + per_page - 1) // per_page  # Вычисляем общее количество страниц

    # Определите диапазон страниц для отображения
    max_page_buttons = 5  # Количество кнопок, отображаемых в пагинации
    start_page = max(1, page - max_page_buttons // 2)
    end_page = min(total_pages, page + max_page_buttons // 2)

    if end_page - start_page < max_page_buttons - 1:
        if start_page > 1:
            end_page = min(total_pages, end_page + (max_page_buttons - (end_page - start_page)))
        else:
            start_page = max(1, end_page - (max_page_buttons - (end_page - start_page)))

    # Отправляем данные на шаблон для отображения
    return render_template(
        'index.html',
        services=services,
        total_cost_1=total_cost_1,
        total_cost_2=total_cost_2,
        total_cost_3=total_cost_3,
        selected_year=year,
        keyword=keyword,
        page=page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        service_years=service_years
    )

# Определяем маршрут для страницы редактирования услуги
@app.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    # Получаем услугу по идентификатору или возвращаем ошибку 404, если услуга не найдена
    service = Service.query.get_or_404(id)  # Ищем услугу по ID

    # Отправляем данные на шаблон для редактирования
    return render_template('edit.html', service=service)

# Определяем маршрут для страницы добавления услуги
@app.route('/add_edit', methods=['GET'])
def add_edit():

    # Отправляем данные на шаблон для добавления
    return render_template('add.html')

from datetime import datetime  # Импортируем datetime для работы с датами

# Определяем маршрут для обновления услуги
@app.route('/edit/<int:id>', methods=['POST'])
def update(id):
    # # Пример проверки длины
    # name = request.form['name']
    # location = request.form['location']
    # address_p = request.form['address_p']
    # address = request.form['address']
    # benefit = request.form['benefit']
    # number = request.form['number']
    # certificate_no = request.form['certificate_no']

    # snils = request.form['snils']
    # cost = request.form['cost']
    # certificate = request.form['certificate']

    # if (len(name) or len(location) or len(address_p) or len(address) or len(benefit) or len(number) or len(certificate_no)) > 30 or (int(snils) or int(cost) or int(certificate)) > 30:
    #     flash('Service Name and Description must be 30 characters or less.')
    #     return redirect(url_for('index'))

    # Получаем услугу по идентификатору или возвращаем ошибку 404, если услуга не найдена
    service = Service.query.get_or_404(id)

    # Обновляем данные услуги на основе данных из формы
    service.name = request.form['name']
    service.snils = request.form['snils']
    service.location = request.form['location']
    service.address_p = request.form['address_p']
    service.address = request.form['address']
    service.benefit = request.form['benefit']
    service.number = request.form['number']
    service.year = datetime.strptime(request.form['year'], '%Y-%m-%d').date()  # Преобразуем строку в дату
    service.cost = request.form['cost']
    service.certificate = request.form['certificate']
    service.date_number_get = request.form['date_number_get']
    service.date_number_cancellation = request.form['date_number_cancellation']
    service.date_number_no = request.form['date_number_no']
    service.certificate_no = request.form['certificate_no']
    service.reason = request.form['reason']
    service.track = request.form['track']
    service.date_post = request.form['date_post']
    service.color = request.form.get('color')  # Получаем значение цвета

    # Сохраняем изменения в базе данных
    db.session.commit()
    flash('Данные успешно обновлены!')  # Отображаем флэш-сообщение об успешном обновлении
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
        'name': service.name,
        'snils': service.snils,
        'location': service.location,
        'address_p': service.address_p,
        'address': service.address,
        'benefit': service.benefit,
        'number': service.number,
        'year': service.year.strftime('%Y-%m-%d') if service.year else None,  # Преобразуем дату в строку
        'cost': service.cost,
        'certificate': service.certificate,
        'date_number_get': service.date_number_get,
        'date_number_cancellation': service.date_number_cancellation,
        'date_number_no': service.date_number_no,
        'certificate_no': service.certificate_no,
        'reason': service.reason,
        'track': service.track,
        'date_post': service.date_post,
        'color': service.color  # Добавляем цвет в ответ
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
    flash('Данные успешно удалены!')

    # Перенаправляем на главную страницу
    return redirect(url_for('index'))

# Определяем маршрут для добавления новой услуги
@app.route('/add', methods=['POST'])
def add():
    # # Пример проверки длины
    # name = request.form['name']
    # location = request.form['location']
    # address_p = request.form['address_p']
    # address = request.form['address']
    # benefit = request.form['benefit']
    # number = request.form['number']
    # certificate_no = request.form['certificate_no']

    # snils = request.form['snils']
    # cost = request.form['cost']
    # certificate = request.form['certificate']

    # print(name)
    # print(location)
    # print(address_p)
    # print(address)
    # print(benefit)
    # print(number)
    # print(certificate_no)
    # print(snils)
    # print(cost)
    # print(certificate)

    # if (len(name) or len(location) or len(address_p) or len(address) or len(benefit) or len(number) or len(certificate_no)) > 30 or (int(snils) or int(cost) or int(certificate)) > 30:
    #     flash('Service Name and Description must be 20 characters or less.')
    #     return redirect(url_for('index'))

    # Получаем данные из формы
    name = request.form['name']
    snils = request.form['snils']
    location = request.form['location']
    address_p = request.form['address_p']
    address = request.form['address']
    benefit = request.form['benefit']
    number = request.form['number']
    year = datetime.strptime(request.form['year'], '%Y-%m-%d').date()  # Преобразуем строку в дату
    cost = request.form['cost']
    certificate = request.form['certificate']
    date_number_get = request.form['date_number_get']
    date_number_cancellation = request.form['date_number_cancellation']
    date_number_no = request.form['date_number_no']
    certificate_no = request.form['certificate_no']
    reason = request.form['reason']
    track = request.form['track']
    date_post = request.form['date_post']
    color = request.form.get('color')  # Получаем значение цвета

    # Создаем новый объект услуги
    new_service = Service(name=name, snils=snils, location=location,
                        address_p=address_p, address=address, benefit=benefit,
                        number=number, year=year, cost=cost,
                        certificate=certificate, date_number_get=date_number_get,
                        date_number_cancellation=date_number_cancellation,
                        date_number_no=date_number_no, certificate_no=certificate_no,
                        reason=reason, track=track, date_post=date_post, color=color)
    db.session.add(new_service)  # Добавляем новый объект в базу данных
    db.session.commit()  # Сохраняем изменения
    flash('Данные успешно добавлены!')  # Отображаем флэш-сообщение об успешном добавлении
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
        'ФИО заявителя': service.name,
        'СНИЛС': service.snils,
        'Район': service.location,
        'Населённый пункт': service.address_p,
        'Адрес': service.address,
        'Льгота': service.benefit,
        'Серия и номер': service.number,
        'Дата выдачи сертификата': service.year.strftime('%Y-%m-%d'),
        'Размер выплаты': service.cost,
        'Сертификат': service.certificate,
        'Дата и номер решения о выдаче': service.date_number_get.strftime('%Y-%m-%d'),
        'Дата и № решения об аннулировании': service.date_number_cancellation.strftime('%Y-%m-%d'),
        'Дата и № решения об отказе в выдаче': service.date_number_no,
        'Отказ в выдаче': service.certificate_no,
        'Причина отказа': service.reason,
        'ТРЕК': service.track,
        'Дата отправки почтой': service.date_post.strftime('%Y-%m-%d'),
        'Color': getattr(service, 'color', '')
    } for service in services])

    # Расчет итогов
    total_cost = df['Размер выплаты'].sum()
    total_certificate = df['Сертификат'].sum()
    total_certificate_no = df['Отказ в выдаче'].sum()

    # Создание строки с итогами
    totals_row = pd.DataFrame([{
        'ФИО заявителя': '',
        'СНИЛС': '',
        'Район': '',
        'Населённый пункт': '',
        'Адрес': '',
        'Льгота': '',
        'Серия и номер': '',
        'Дата выдачи сертификата': '',
        'Размер выплаты': total_cost,
        'Сертификат': total_certificate,
        'Дата и номер решения о выдаче': '',
        'Дата и № решения об аннулировании': '',
        'Дата и № решения об отказе в выдаче': '',
        'Отказ в выдаче': total_certificate_no,
        'Причина отказа': '',
        'ТРЕК': '',
        'Дата отправки почтой': '',
        'Color': ''
    }])

    # Добавление строки с итогами в DataFrame
    df = pd.concat([df, totals_row], ignore_index=True)

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

        # Определяем стиль для заливки желтым цветом
        yellow_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

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

        # Применяем желтый цвет к строке с итогами
        totals_row_num = worksheet.max_row
        for col_num in range(1, worksheet.max_column + 1):
            cell = worksheet.cell(row=totals_row_num, column=col_num)
            cell.fill = yellow_fill
            cell.border = border_style

        # Удаляем столбец Color из Excel-файла
        worksheet.delete_cols(df.columns.get_loc("Color") + 1)

    output.seek(0)

    # Отправляем файл пользователю
    return send_file(output, as_attachment=True, download_name='services.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# Запускаем приложение в режиме отладки
if __name__ == '__main__':
    app.run(debug=True)  # Запускаем сервер Flask с режимом отладки
