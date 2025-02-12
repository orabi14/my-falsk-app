import os
import logging
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Initialize Flask application using factory pattern
def create_app():
    app = Flask(__name__)

    # Configuration
    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev-secret-key'),
        WTF_CSRF_SECRET_KEY=os.getenv('CSRF_SECRET_KEY', 'csrf-secret-key'),
        ENV=os.getenv('FLASK_ENV', 'production'),
        DEBUG=os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    )

    # Form classes
    class ContactForm(FlaskForm):
        name = StringField(
            'Name', [validators.InputRequired(), validators.Length(min=2, max=50)]
        )
        email = StringField(
            'Email', [validators.InputRequired(), validators.Email()]
        )
        message = TextAreaField(
            'Message', [validators.InputRequired(), validators.Length(min=10, max=500)]
        )

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'Server Error: {error}')
        return render_template('errors/500.html'), 500

    # Routes
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            try:
                name = form.name.data
                email = form.email.data
                message = form.message.data

                # Log message instead of print
                logger.info(f"New contact message from {name} ({email}): {message}")

                # TODO: Add email sending logic here
                # TODO: Store message in database

                flash('Your message has been sent successfully!', 'success')
                return redirect(url_for('home'))

            except Exception as e:
                logger.error(f"Error processing contact form: {str(e)}")
                flash('An error occurred while sending your message. Please try again.', 'danger')
                return redirect(url_for('contact'))

        return render_template('contact.html', form=form)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000))
    )
