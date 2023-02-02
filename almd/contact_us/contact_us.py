from flask import Blueprint, render_template, url_for, redirect
from almd.forms.forms import ContactForm
import os
import smtplib


contact_bp = Blueprint(
    'contact_bp', __name__, template_folder='templates',
    static_folder='static',
    static_url_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
)  # create blueprint inorder to render the news package


@contact_bp.route('/', methods=["POST", "GET"])
def contact_us():
    form = ContactForm()
    admin_email = os.environ['ADMIN_EMAIL']
    admin_password = os.environ['ADMIN_EMAIL_PASSWORD']

    if form.validate_on_submit():
        client_name = form.name.data
        client_email = form.email.data
        client_message = form.message.data

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(  # log in to email address for sending email
                user=admin_email,
                password=admin_password
            )
            connection.sendmail(
                from_addr=admin_email,
                to_addrs=admin_email,
                msg=f"Subject: Some Subject\n\n Message from: {client_name}\n "
                f"Email:{client_email}\n\n{client_message}"
            )
        return redirect(url_for('home'))  #there should be some redirecting taking place here
    return render_template('contact-us/contact-us.html', form=form)
