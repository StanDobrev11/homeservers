from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a real secret key in production
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your-password'  # Replace with your password
app.config['MAIL_DEFAULT_SENDER'] = ('NAS Builder', 'your-email@example.com')

mail = Mail(app)

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
    
    # Create email message
    user_msg = Message(
        subject='Your NAS Build Request',
        recipients=[email],
        body=f"""
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
    )
    
    owner_msg = Message(
        subject=f'New NAS Build Request from {name}',
        recipients=['your-email@example.com'],  # Replace with your email
        body=f"""
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
    )
    
    # Send emails
    try:
        mail.send(user_msg)
        mail.send(owner_msg)
        flash('Your request has been submitted successfully! Check your email for confirmation.', 'success')
    except Exception as e:
        flash(f'There was an error sending your request: {str(e)}', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)