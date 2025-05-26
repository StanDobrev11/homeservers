from flask import Flask, render_template, request, redirect, url_for, flash, g, session
from flask_babel import Babel
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect  # Import CSRFProtect
import os
from dotenv import load_dotenv
import logging
import uuid
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize visitor tracking
visitor_count = 0
visitors = {}

# Initialize Flask app with explicit static_folder
app = Flask(__name__,
            static_folder='static',  # Explicitly define static folder
            static_url_path='/static')  # Explicit URL path for static files

# Configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-dev-key')

# Initialize CSRF protection
csrf = CSRFProtect(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True

# Babel configuration
app.config['BABEL_DEFAULT_LOCALE'] = 'bg'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'bg']
app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'translations')

SENDER_NAME = os.getenv('SENDER_NAME')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

# SMTP config
app.config['MAIL_SERVER'] = 'smtp-relay.brevo.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = (SENDER_NAME, SENDER_EMAIL)

mail = Mail(app)

def get_locale():
    # 1. Check if language is set in session
    if 'language' in session:
        logger.debug(f"Language from session: {session['language']}")
        return session['language']

    # 2. Check browser preference
    best_match = request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])
    if best_match:
        logger.debug(f"Language from browser: {best_match}")
        return best_match
    
    # 3. Fall back to default locale
    default_locale = app.config['BABEL_DEFAULT_LOCALE']
    logger.debug(f"Using default locale: {default_locale}")
    return default_locale


# Remove mail initialization
# mail = Mail(app)
babel = Babel()
babel.init_app(app, locale_selector=get_locale)

def get_admin_emails():
    """Parse the ADMIN_EMAIL env var into a list of valid email addresses."""
    if not ADMIN_EMAIL:
        return []
    # Split by spaces or commas
    emails = []
    for part in ADMIN_EMAIL.replace(',', ' ').split():
        if '@' in part:  # Simple validation
            emails.append(part.strip())
    return emails


def send_email(to_email, subject, html_content, text_content=None):
    """
    Send email using Flask-Mail and Brevo SMTP settings.
    """

    # Handle recipient list
    if isinstance(to_email, list):
        recipients = [email.strip() for email in to_email if isinstance(email, str) and '@' in email]
    elif isinstance(to_email, str) and '@' in to_email:
        recipients = [to_email.strip()]
    else:
        error_msg = f"Invalid email address: {to_email}"
        logger.error(error_msg)
        return False, error_msg

    if not recipients:
        error_msg = "No valid recipient email addresses found"
        logger.error(error_msg)
        return False, error_msg

    try:
        msg = Message(subject=subject, recipients=recipients)
        msg.body = text_content or html_content
        msg.html = html_content

        mail.send(msg)
        logger.debug(f"Email sent successfully to: {recipients}")
        return True, None
    except Exception as e:
        error_msg = f"Failed to send email: {e}"
        logger.error(error_msg)
        return False, error_msg


@app.before_request
def before_request():
    global visitor_count, visitors
    
    # Set default language in session if not already set (first visit)
    if 'language' not in session:
        session['language'] = app.config['BABEL_DEFAULT_LOCALE']
        logger.debug(f"Setting default language in session: {session['language']}")
    
    # Visitor tracking
    if 'visitor_id' not in session:
        # Generate a unique visitor ID
        visitor_id = str(uuid.uuid4())
        session['visitor_id'] = visitor_id
        visitor_count += 1
        
        # Store visitor info
        visitors[visitor_id] = {
            'first_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ip': request.remote_addr,
            'user_agent': request.user_agent.string,
            'language': session['language']
        }
        
        logger.debug(f"New visitor! Total unique visitors: {visitor_count}")
        logger.debug(f"Visitor info: {visitors[visitor_id]}")
    
    # Set locale for this request
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

@app.route('/stats', methods=['GET'])
def visitor_stats():
    # This is a simple debug route to view visitor statistics
    # In a production environment, you would want to secure this with authentication
    if app.debug:
        return {
            'total_unique_visitors': visitor_count,
            'active_sessions': len(visitors),
            'visitors': visitors
        }
    else:
        return "Stats only available in debug mode", 403

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

    # Log received data
    logger.debug(f"Form submitted by: {name} <{email}> - {phone}")

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

    try:
        # Send to user
        success_user, error_user = send_email(
            to_email=email,
            subject=user_subject,
            html_content=user_body,
            text_content=user_text
        )

        # Get admin emails
        admin_emails = get_admin_emails()
        if not admin_emails:
            logger.warning("No valid admin emails configured. Cannot send notification.")

        # Send to admin
        success_admin, error_admin = False, None
        if admin_emails:
            success_admin, error_admin = send_email(
                to_email=admin_emails,
                subject=owner_subject,
                html_content=owner_body,
                text_content=owner_text
            )

        # Handle success/failure
        if success_user and (success_admin or not admin_emails):
            flash(success_message, 'success')
        else:
            error_details = error_user or error_admin
            flash(f'{error_message} {error_details}', 'error')

    except Exception as e:
        logger.exception("Unexpected error when sending emails")
        flash(f'{error_message} {str(e)}', 'error')

    return redirect(url_for('index'))


if __name__ == '__main__':
    # Use 0.0.0.0 to listen on all interfaces
    app.run(host='0.0.0.0', port=5000, debug=False)
