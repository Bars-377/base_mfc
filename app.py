from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Service
from datetime import datetime
import pandas as pd
from io import BytesIO
from flask import send_file
from openpyxl.styles import PatternFill, Border, Side

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:enigma1418@localhost/mdtomskbot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    year = request.args.get('year', None)
    keyword = request.args.get('keyword', None)
    selected_column = request.args.get('column', None)
    page = request.args.get('page', 1, type=int)
    per_page = 20

    service_years = db.session.query(db.func.year(Service.year)).distinct().all()
    service_years = [str(year[0]) for year in service_years]

    query = Service.query

    print(year)
    print(type(year))

    if year == 'No':
        year = None

    if year:
        if year != 'None':
            # year = int(year)
            query = query.filter(db.func.year(Service.year) == year)

    if keyword:
        if selected_column and hasattr(Service, selected_column):
            column = getattr(Service, selected_column)
            query = query.filter(column.like(f'%{keyword}%'))
        else:
            columns = [c for c in Service.__table__.columns.keys()]
            filters = [getattr(Service, col).like(f'%{keyword}%') for col in columns]
            query = query.filter(db.or_(*filters))

    """ДОДЕЛАТЬ"""
    # query = query.order_by(Service.id_id.asc(), Service.year.asc())

    if year:
        query = query.order_by(Service.id_id.asc(), Service.year.asc())
    else:
        query = query.order_by(Service.id_id.asc())

    total_cost_1 = db.session.query(db.func.sum(Service.cost)).scalar() or 0
    total_cost_2 = db.session.query(db.func.sum(Service.certificate)).scalar() or 0
    total_cost_3 = db.session.query(db.func.sum(Service.certificate_no)).scalar() or 0

    offset = (page - 1) * per_page
    services = query.offset(offset).limit(per_page).all()
    total_services = query.count()
    total_pages = (total_services + per_page - 1) // per_page

    max_page_buttons = 5
    start_page = max(1, page - max_page_buttons // 2)
    end_page = min(total_pages, page + max_page_buttons // 2)

    if end_page - start_page < max_page_buttons - 1:
        if start_page > 1:
            end_page = min(total_pages, end_page + (max_page_buttons - (end_page - start_page)))
        else:
            start_page = max(1, end_page - (max_page_buttons - (end_page - start_page)))

    return render_template(
        'index.html',
        services=services,
        total_cost_1=total_cost_1,
        total_cost_2=total_cost_2,
        total_cost_3=total_cost_3,
        selected_year=year,
        selected_column=selected_column,
        keyword=keyword,
        page=page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        service_years=service_years
    )

@app.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    service = Service.query.get_or_404(id)
    return render_template('edit.html', service=service)

@app.route('/add_edit', methods=['GET'])
def add_edit():
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['POST'])
def update(id):
    service = Service.query.get_or_404(id)
    service.id_id = request.form['id_id']
    service.name = request.form['name']
    service.snils = request.form['snils']
    service.location = request.form['location']
    service.address_p = request.form['address_p']
    service.address = request.form['address']
    service.benefit = request.form['benefit']
    service.number = request.form['number']
    service.year = datetime.strptime(request.form['year'], '%Y-%m-%d').date()
    service.cost = request.form['cost']
    service.certificate = request.form['certificate']
    service.date_number_get = request.form['date_number_get']
    service.date_number_cancellation = request.form['date_number_cancellation']
    service.date_number_no = request.form['date_number_no']
    service.certificate_no = request.form['certificate_no']
    service.reason = request.form['reason']
    service.track = request.form['track']
    service.date_post = request.form['date_post']
    service.color = request.form.get('color')

    db.session.commit()
    flash('Данные успешно обновлены!')
    return redirect(url_for('index'))

@app.route('/update-color/<int:id>', methods=['POST'])
def update_color(id):
    service = Service.query.get_or_404(id)
    data = request.json
    color = data.get('color')

    if color:
        service.color = color
        db.session.commit()
        return jsonify({
            'success': True,
            'id': service.id,
            'color': service.color
        })
    else:
        return jsonify({'success': False, 'message': 'No color provided'}), 400

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash('Данные успешно удалены!')
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add():
    id_id = request.form['id_id']
    name = request.form['name']
    snils = request.form['snils']
    location = request.form['location']
    address_p = request.form['address_p']
    address = request.form['address']
    benefit = request.form['benefit']
    number = request.form['number']
    year = datetime.strptime(request.form['year'], '%Y-%m-%d').date()
    cost = request.form['cost']
    certificate = request.form['certificate']
    date_number_get = request.form['date_number_get']
    date_number_cancellation = request.form['date_number_cancellation']
    date_number_no = request.form['date_number_no']
    certificate_no = request.form['certificate_no']
    reason = request.form['reason']
    track = request.form['track']
    date_post = request.form['date_post']
    color = request.form.get('color')

    new_service = Service(id_id=id_id, name=name, snils=snils, location=location,
                        address_p=address_p, address=address, benefit=benefit,
                        number=number, year=year, cost=cost,
                        certificate=certificate, date_number_get=date_number_get,
                        date_number_cancellation=date_number_cancellation,
                        date_number_no=date_number_no, certificate_no=certificate_no,
                        reason=reason, track=track, date_post=date_post, color=color)
    db.session.add(new_service)
    db.session.commit()
    flash('Данные успешно добавлены!')
    return redirect(url_for('index'))

@app.route('/export-excel', methods=['GET'])
def export_excel():
    year = request.args.get('year', None)

    query = Service.query
    if year and year.isdigit():
        query = query.filter(db.func.year(Service.year) == int(year))

    services = query.all()

    df = pd.DataFrame([{
        '№ п/п': service.id_id,
        'ФИО заявителя': service.name,
        'СНИЛС': service.snils,
        'Район': service.location,
        'Адрес заявителя': service.address_p,
        'Адрес': service.address,
        'Льготы': service.benefit,
        'Номер договора': service.number,
        'Дата документа': service.year,
        'Стоимость': service.cost,
        'Сертификат': service.certificate,
        'Дата получения': service.date_number_get,
        'Дата аннулирования': service.date_number_cancellation,
        'Дата неопределённости': service.date_number_no,
        'Сертификат (неопределённость)': service.certificate_no,
        'Причина аннулирования': service.reason,
        'Трек': service.track,
        'Дата поста': service.date_post,
        'Цвет': service.color
    } for service in services])

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Services')

        worksheet = writer.sheets['Services']

        header_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
        for cell in worksheet[1]:
            cell.fill = header_fill

        for row in worksheet.iter_rows(min_row=2, max_col=len(df.columns)):
            for cell in row:
                cell.border = Border(left=Side(border_style='thin'),
                                    right=Side(border_style='thin'),
                                    top=Side(border_style='thin'),
                                    bottom=Side(border_style='thin'))

    output.seek(0)
    return send_file(output, download_name="services.xlsx", as_attachment=True)

"""Nginx"""
from waitress import serve
if __name__ == '__main__':
    serve(app, host='172.18.88.41', port=8000)

"""Standart"""
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
