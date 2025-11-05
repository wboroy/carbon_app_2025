from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from capp.models import Transport
from capp import db
from datetime import timedelta, datetime
from capp.carbon_app.forms import BusForm

carbon_app=Blueprint('carbon_app',__name__)


efco2={'Bus':{'Diesel':0.10,'CNG':0.08, 'Petrol':0.15,'No Fossil Fuel':0}}
efch4={'Bus':{'Diesel':0.20,'CNG':0.08, 'Petrol':0.30,'No Fossil Fuel':0}}


@carbon_app.route('/carbon_app')
@login_required
def carbon_app_home():
    return render_template('carbon_app/carbon_app.html', title='carbon_app')

@carbon_app.route('/carbon_app/new_entry_bus', methods=['GET','POST'])
@login_required
def new_entry():
    form =BusForm()
    if form.validate_on_submit():
        kms=form.kms.data
        fuel=form.fuel_type.data
        transport='Bus'
        co2=float(kms)*efco2[transport][fuel]
        ch4=float(kms)*efch4[transport][fuel]
        total=co2+ch4
        co2=float("{:.2f}".format(co2))
        ch4=float("{:.2f}".format(ch4))
        total=float("{:.2f}".format(total))
        emissions=Transport(kms=kms, transport=transport, fuel=fuel,
                            co2=co2, ch4=ch4, total=total, author=current_user)
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_app.your_data'))
    return render_template('carbon_app/new_entry_bus.html', title='new_entry_bus', form=form)

@carbon_app.route('/carbon_app/your_data')
@login_required
def your_data():
    entries = Transport.query.filter_by(author=current_user).\
        filter(Transport.date>(datetime.now()-timedelta(days=5))).\
        order_by(Transport.date.desc()).order_by(Transport.transport.asc()).all()
    return render_template('carbon_app/your_data.html', title='your_data', entries=entries)
@carbon_app.route('/carbon_app/delete_emissions/<int:entry_id>')
def delete_emission(entry_id):
    entry=Transport.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted","sucsess")
    return redirect(url_for('carbon_app.your_data'))

    