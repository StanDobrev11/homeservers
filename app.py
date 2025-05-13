from flask import Flask, render_template, request, redirect, url_for, flash, g, session
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect  # Import CSRFProtect
import os
from dotenv import load_dotenv
import logging

# Import Brevo's SDK
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app with explicit static_folder
app = Flask(__name__,
            static_folder='static',  # Explicitly define static folder
            static_url_path='/static')  # Explicit URL path for static files

# Configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-dev-key')

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Replace MailHog configuration with Brevo API key
BREVO_API_KEY = os.getenv('BREVO_API_KEY')
SENDER_NAME = os.getenv('SENDER_NAME', 'NAS Builder')
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'no-reply@cloudmachine.uk')

app.config['TEMPLATES_AUTO_RELOAD'] = True

# Babel configuration
app.config['BABEL_DEFAULT_LOCALE'] = 'bg'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'bg']
app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'translations')

# Admin email for receiving form submissions
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'dobrev81@gmail.com Alexander_Zarchev@cargill.com')


def get_locale():
    if 'language' in session:
        logger.debug(f"Language from session: {session['language']}")
        return session['language']

    best_match = request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])
    logger.debug(f"Language from browser: {best_match}")
    return best_match


# Remove mail initialization
# mail = Mail(app)
babel = Babel()
babel.init_app(app, locale_selector=get_locale)


# Add function to send email with Brevo
def send_email(to_email, subject, html_content, text_content=None):
    """
    Send email using Brevo API
    """
    # Configure API key authorization
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = BREVO_API_KEY

    # Create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Define sender and recipient
    sender = {"name": SENDER_NAME, "email": SENDER_EMAIL}
    to = [{"email": to_email}]

    # Create SendSmtpEmail object
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        sender=sender,
        subject=subject,
        html_content=html_content,
        text_content=text_content or html_content
    )

    try:
        # Send the email
        api_response = api_instance.send_transac_email(send_smtp_email)
        logger.debug(f"Email sent successfully: {api_response}")
        return True, None
    except ApiException as e:
        error_msg = f"Exception when calling Brevo API: {e}"
        logger.error(error_msg)
        return False, error_msg


@app.before_request
def before_request():
    g.locale = get_locale()


@app.route('/language/<language>')
def set_language(language):
    if language in ['en', 'bg']:
        session['language'] = language  # Set the language in the session
    return redirect(request.referrer or url_for('index'))  # Redirect to the previous page


@app.route('/', methods=['GET'])
def index():
    return render_template('landing.html')


@app.route('/request', methods=['GET'])
def request_form():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    # Get form data
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    usage_type = request.form.get('usage_type')
    storage_needs = request.form.get('storage_needs')
    backup_plans = request.form.get('backup_plans')
    budget = request.form.get('budget')
    comments = request.form.get('comments')

    # Get the current locale for email content
    current_locale = get_locale()

    # Create email content with translated content
    if current_locale == 'bg':
        user_subject = 'Вашата заявка за NAS система'
        user_body = f"""
        <html>
        <body>
        <p>Благодарим за вашата заявка за NAS система, {name}!</p>
        <p>Получихме вашите изисквания и ще се свържем с вас скоро.</p>
        <h3>Детайли на вашата заявка:</h3>
        <ul>
            <li>Тип на използване: {usage_type}</li>
            <li>Нужди за съхранение: {storage_needs}</li>
            <li>План за резервно копие: {backup_plans}</li>
            <li>Бюджет: {budget}</li>
            <li>Допълнителни коментари: {comments}</li>
        </ul>
        <p>С уважение,<br>
        Екипът на NAS Builder</p>
        </body>
        </html>
        """

        user_text = f"""
        Благодарим за вашата заявка за NAS система, {name}!

        Получихме вашите изисквания и ще се свържем с вас скоро.

        Детайли на вашата заявка:
        - Тип на използване: {usage_type}
        - Нужди за съхранение: {storage_needs}
        - План за резервно копие: {backup_plans}
        - Бюджет: {budget}
        - Допълнителни коментари: {comments}

        С уважение,
        Екипът на NAS Builder
        """

        owner_subject = f'Нова заявка за NAS система от {name}'
        owner_body = f"""
        <html>
        <body>
        <h2>Нова заявка за NAS система:</h2>
        <h3>Информация за клиента:</h3>
        <ul>
            <li>Име: {name}</li>
            <li>Имейл: {email}</li>
            <li>Телефон: {phone}</li>
        </ul>
        <h3>Изисквания:</h3>
        <ul>
            <li>Тип на използване: {usage_type}</li>
            <li>Нужди за съхранение: {storage_needs}</li>
            <li>План за резервно копие: {backup_plans}</li>
            <li>Бюджет: {budget}</li>
            <li>Допълнителни коментари: {comments}</li>
        </ul>
        </body>
        </html>
        """

        owner_text = f"""
        Нова заявка за NAS система:

        Информация за клиента:
        - Име: {name}
        - Имейл: {email}
        - Телефон: {phone}

        Изисквания:
        - Тип на използване: {usage_type}
        - Нужди за съхранение: {storage_needs}
        - План за резервно копие: {backup_plans}
        - Бюджет: {budget}
        - Допълнителни коментари: {comments}
        """

        success_message = 'Вашата заявка беше изпратена успешно! Проверете имейла си за потвърждение.'
        error_message = 'Възникна грешка при изпращане на заявката: '
    else:
        user_subject = 'Your NAS Build Request'
        user_body = f"""
        <html>
        <body>
        <p>Thank you for your NAS build request, {name}!</p>
        <p>We have received your requirements and will get back to you shortly.</p>
        <h3>Your request details:</h3>
        <ul>
            <li>Usage Type: {usage_type}</li>
            <li>Storage Needs: {storage_needs}</li>
            <li>Backup Plans: {backup_plans}</li>
            <li>Budget: {budget}</li>
            <li>Additional Comments: {comments}</li>
        </ul>
        <p>Best regards,<br>
        The NAS Builder Team</p>
        </body>
        </html>
        """

        user_text = f"""
        Thank you for your NAS build request, {name}!

        We have received your requirements and will get back to you shortly.

        Your request details:
        - Usage Type: {usage_type}
        - Storage Needs: {storage_needs}
        - Backup Plans: {backup_plans}
        - Budget: {budget}
        - Additional Comments: {comments}

        Best regards,
        The NAS Builder Team
        """

        owner_subject = f'New NAS Build Request from {name}'
        owner_body = f"""
        <html>
        <body>
        <h2>New NAS build request:</h2>
        <h3>Customer Information:</h3>
        <ul>
            <li>Name: {name}</li>
            <li>Email: {email}</li>
            <li>Phone: {phone}</li>
        </ul>
        <h3>Requirements:</h3>
        <ul>
            <li>Usage Type: {usage_type}</li>
            <li>Storage Needs: {storage_needs}</li>
            <li>Backup Plans: {backup_plans}</li>
            <li>Budget: {budget}</li>
            <li>Additional Comments: {comments}</li>
        </ul>
        </body>
        </html>
        """

        owner_text = f"""
        New NAS build request:

        Customer Information:
        - Name: {name}
        - Email: {email}
        - Phone: {phone}

        Requirements:
        - Usage Type: {usage_type}
        - Storage Needs: {storage_needs}
        - Backup Plans: {backup_plans}
        - Budget: {budget}
        - Additional Comments: {comments}
        """

        success_message = 'Your request has been submitted successfully! Check your email for confirmation.'
        error_message = 'There was an error sending your request: '

    # Send emails using Brevo
    try:
        # Send to user
        success_user, error_user = send_email(
            to_email=email,
            subject=user_subject,
            html_content=user_body,
            text_content=user_text
        )

        # Send to admin
        success_admin, error_admin = send_email(
            to_email=[email for email in ADMIN_EMAIL.split(' ')],
            subject=owner_subject,
            html_content=owner_body,
            text_content=owner_text
        )

        if success_user and success_admin:
            flash(success_message, 'success')
        else:
            error_details = error_user or error_admin
            flash(f'{error_message} {error_details}', 'error')

    except Exception as e:
        flash(f'{error_message} {str(e)}', 'error')

    return redirect(url_for('index'))


if __name__ == '__main__':
    # Use 0.0.0.0 to listen on all interfaces
    app.run(host='0.0.0.0', port=5000, debug=False)
