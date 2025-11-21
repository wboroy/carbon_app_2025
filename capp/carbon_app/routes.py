from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from capp.models import Transport
from capp import db
from datetime import timedelta, datetime, date
from capp.carbon_app.forms import TransportForm
import json

carbon_app=Blueprint('carbon_app',__name__)

#dictionary
efco2={'Bus':{'Diesel':0.03, 'Electric':0.013},
       'Car':{'Diesel':0.229, 'Petrol': 0.198, 'Electric':0.059},
       'Motorbike':{'Fossil fuel':0.095},
       'Train':{'Diesel':0.091,'Electric':0.007},
       'Plane Economy':{'Jetfuel':0.127},
       'Plane Business':{'Jetfuel':0.284},
       'Ferry':{'Fossil fuel':0.186, 'Electric':0.023},
       'Bybane':{'Electric':0.0015},
       'Walking/Cycling':{'Human powered':0}
}



@carbon_app.route('/carbon_app', methods=['GET','POST'])
@login_required
def carbon_app_home():
    form =TransportForm()
    if form.validate_on_submit():
        kms=form.kms.data
        fuel=form.fuel_type.data
        transport= form.transport.data
        
        passengers = form.passenger.data if form.passenger.data else 1
        
        co2=float(kms)*efco2[transport][fuel]
        
        if transport in ["Car","Motorbike"]:
            co2 = co2 / passengers
        
        total = co2
        co2=float("{:.2f}".format(co2))
        total=float("{:.2f}".format(total))
        emissions=Transport(kms=kms, transport=transport, fuel=fuel,
                            co2=co2, total=total, author=current_user)
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
    
    #sier til databasen "add alle co2 tall sammen men sorter dem etter transport type", så summen av totale buss utslipp, summen av totale bil utslipp, ect
    #Bruker bare siste 5 dager
    #Grupperer transport sammen og alfabetisk for pie diagrammet
    emissions_by_transport = db.session.query(
        db.func.sum(Transport.total), Transport.transport). \
        filter(Transport.date > (datetime.now() - timedelta(days=5))).filter_by(author=current_user). \
        group_by(Transport.transport).order_by(Transport.transport.asc()).all()

    # Konverterer data til lister
    emission_dict = {}
    for value, transport in emissions_by_transport:
        emission_dict[transport] = value

    emission_value = list(emission_dict.values())
    emissions_lable = list(emission_dict.keys())

    #Emissions by date (individual)
    emissions_by_date = db.session.query(db.func.sum(Transport.total), Transport.date). \
        filter(Transport.date > (datetime.now() - timedelta(days=5))).filter_by(author=current_user). \
        group_by(Transport.date).order_by(Transport.date.asc()).all()
    over_time_emissions = []
    dates_label = []
    for total, date in emissions_by_date:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_emissions.append(total)    

    #for kilometers     
    kms_by_transport = db.session.query(db.func.sum(Transport.kms), Transport.transport). \
        filter(Transport.date > (datetime.now() - timedelta(days=5))).filter_by(author=current_user). \
        group_by(Transport.transport).order_by(Transport.transport.asc()).all()

    # kms transport pie chart
    kms_dict = {}
    for value, transport in kms_by_transport:
        kms_dict[transport] = value

    kms_values = list(kms_dict.values())
    kms_lable = list(kms_dict.keys())


        # Kilometers by date
    kms_by_date = db.session.query(db.func.sum(Transport.kms), Transport.date). \
        filter(Transport.date > (datetime.now() - timedelta(days=5))).filter_by(author=current_user). \
        group_by(Transport.date).order_by(Transport.date.asc()).all()

    kms_over_time = []
    for kms, date in kms_by_date:
        kms_over_time.append(kms)


#sender til html via json
    return render_template('carbon_app/your_data.html', title='your_data', 
        entries=entries,
        emissions_by_transport=json.dumps(emission_value),
        transport_labels=json.dumps(emissions_lable),
        over_time_emissions=json.dumps(over_time_emissions),
        dates_label=json.dumps(dates_label),
        kms_over_time=json.dumps(kms_over_time),
        kms_by_transport=json.dumps(kms_values),
        kms_labels=json.dumps(kms_lable))
    

#Sletter fra databasen hvis brukeren ønsker det
@carbon_app.route('/carbon_app/delete_emissions/<int:entry_id>')
def delete_emission(entry_id):
    entry=Transport.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted","sucsess")
    return redirect(url_for('carbon_app.your_data'))
