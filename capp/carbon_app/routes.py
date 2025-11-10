from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from capp.models import Transport
from capp import db
from datetime import timedelta, datetime, date
from capp.carbon_app.forms import TransportForm

carbon_app=Blueprint('carbon_app',__name__)


efco2={'Bus':{'Diesel':0.10,'CNG':0.08, 'Petrol':0.15,'No Fossil Fuel':0},

       'Car':{'Diesel':2, 'Petrol': 3}
}

efch4={'Bus':{'Diesel':0.20,'CNG':0.08, 'Petrol':0.30,'No Fossil Fuel':0},
       'Car':{'Diesel':0.20,'Petrol':0.3}
}



@carbon_app.route('/carbon_app', methods=['GET','POST'])
@login_required
def carbon_app_home():
    form =TransportForm()
    if form.validate_on_submit():
        kms=form.kms.data
        fuel=form.fuel_type.data
        transport= form. transport.data
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
    return render_template('carbon_app/carbon_app.html', title='Carbon App', form=form)


#Viser brukeren dataen siste 5 dagene og sorterer etter nyest til gamlest
@carbon_app.route('/carbon_app/your_data')
@login_required
def your_data():
    entries = Transport.query.filter_by(author=current_user).\
        filter(Transport.date>(datetime.now()-timedelta(days=5))).\
        order_by(Transport.date.desc()).order_by(Transport.transport.asc()).all()
    return render_template('carbon_app/your_data.html', title='your_data', entries=entries)

#Sletter fra databasen hvis brukeren ønsker det
@carbon_app.route('/carbon_app/delete_emissions/<int:entry_id>')
def delete_emission(entry_id):
    entry=Transport.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted","sucsess")
    return redirect(url_for('carbon_app.your_data'))

    