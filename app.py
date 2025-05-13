from flask import Flask, render_template, request, redirect, url_for, flash, g, session
from flask_mail import Mail, Message
from flask_babel import Babel, gettext as _, get_locale
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-dev-key')

# MailHog Configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 1025))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'False').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME') if os.getenv('MAIL_USERNAME') != 'None' else None
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD') if os.getenv('MAIL_PASSWORD') != 'None' else None
app.config['MAIL_DEFAULT_SENDER'] = (
    os.getenv('MAIL_DEFAULT_SENDER_NAME', 'NAS Builder'),
    os.getenv('MAIL_DEFAULT_SENDER_EMAIL', 'nasbuilder@example.com')
)

# Babel configuration
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'bg']
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

# Admin email for receiving form submissions
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.com')

mail = Mail(app)
babel = Babel(app)


def get_locale():
    # Try to get the language from the session
    if 'language' in session:
        return session['language']

    # If not in session, try to detect from browser
    return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])


# Register the locale selector function with Babel
babel.locale_selector_func = get_locale


@app.route('/language/<language>')
def set_language(language):
    session['language'] = language
    return redirect(request.referrer or url_for('index'))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    # Get form data
    name = request.form.get('name')
    email = request.form.get('email')
    usage_type = request.form.get('usage_type')
    storage_needs = request.form.get('storage_needs')
    backup_plans = request.form.get('backup_plans')
    budget = request.form.get('budget')
    comments = request.form.get('comments')

    # Get the current locale for email content
    current_locale = get_locale()

    # Create email messages with translated content
    if current_locale == 'bg':
        user_subject = 'Вашата заявка за NAS система'
        user_body = f"""
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
        Нова заявка за NAS система:

        Информация за клиента:
        - Име: {name}
        - Имейл: {email}

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
        New NAS build request:

        Customer Information:
        - Name: {name}
        - Email: {email}

        Requirements:
        - Usage Type: {usage_type}
        - Storage Needs: {storage_needs}
        - Backup Plans: {backup_plans}
        - Budget: {budget}
        - Additional Comments: {comments}
        """

        success_message = 'Your request has been submitted successfully! Check your email for confirmation.'
        error_message = 'There was an error sending your request: '

    user_msg = Message(
        subject=user_subject,
        recipients=[email],
        body=user_body
    )

    owner_msg = Message(
        subject=owner_subject,
        recipients=[ADMIN_EMAIL],
        body=owner_body
    )

    # Send emails
    try:
        mail.send(user_msg)
        mail.send(owner_msg)
        flash(success_message, 'success')
    except Exception as e:
        flash(f'{error_message} {str(e)}', 'error')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)