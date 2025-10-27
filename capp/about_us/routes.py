from flask import render_template, Blueprint

about_us=Blueprint('about_us',__name__)

@about_us.route('/about_us')
def about_us_home():
  return render_template('About_us.html', title='About Us')