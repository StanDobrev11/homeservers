# HomeServers - Custom NAS Builder
A web application for requesting personalized NAS (Network Attached Storage) build recommendations tailored to individual needs. This project helps users specify their requirements and receive custom NAS configurations.
## Features
- **Multi-language Support**: Available in English and Bulgarian
- **Custom NAS Request Form**: Easy-to-use interface for specifying requirements
- **Email Notifications**: Automated email system to notify users and administrators
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack
- **Backend**: Flask (Python web framework)
- **Frontend**: HTML, CSS, JavaScript
- **Email Service**: Brevo API for transactional emails
- **Internationalization**: Flask-Babel for multi-language support
- **Deployment**: Docker and Docker Compose for containerization

## Getting Started
### Prerequisites
- Docker and Docker Compose installed on your system
- Brevo API key for email functionality

### Installation
1. Clone the repository:
``` bash
   git clone https://github.com/yourusername/homeservers.git
   cd homeservers
```
2. Create a `.env` file in the project root with the following variables:
``` 
   # Brevo API settings
   BREVO_API_KEY=your-brevo-api-key
   SENDER_NAME=NAS Builder
   SENDER_EMAIL=your-verified-sender@domain.com

   # Security
   SECRET_KEY=a-secure-random-string

   # Admin contact
   ADMIN_EMAIL=admin1@example.com,admin2@example.com

   # Server settings
   SERVER_NAME=your-domain.com
```
3. Build and run the Docker container:
``` bash
   docker-compose up -d
```
4. Access the application at `http://localhost:5000`

## Development
### Local Setup
1. Create a virtual environment:
``` bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
2. Install dependencies:
``` bash
   pip install -r requirements.txt
```
3. Run the application in development mode:
``` bash
   flask run --debug
```
### Translation Workflow
To update translations:
1. Extract translatable strings:
``` bash
   pybabel extract -F babel.cfg -o messages.pot .
```
2. Create or update Bulgarian translations:
``` bash
   # Initialize (first time)
   pybabel init -i messages.pot -d translations -l bg
   
   # Update (subsequent times)
   pybabel update -i messages.pot -d translations
```
3. Edit translations/bg/LC_MESSAGES/messages.po
4. Compile translations:
``` bash
   pybabel compile -d translations
```
## Production Deployment
For production deployment:
1. Set proper environment variables in your `.env` file
2. Make sure to use strong, unique SECRET_KEY
3. Enable HTTPS by using a reverse proxy like Nginx with SSL certificates
4. Deploy using Docker Compose:
``` bash
   docker-compose up -d
```
## Project Structure
``` 
homeservers/
├── app.py             # Main Flask application
├── babel.cfg          # Babel configuration
├── Dockerfile         # Docker configuration
├── docker-compose.yaml  # Docker Compose setup
├── requirements.txt   # Python dependencies
├── static/            # Static assets (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── icons/
├── templates/         # HTML templates
│   ├── base.html      # Base template
│   ├── form.html      # NAS request form
│   └── landing.html   # Homepage
└── translations/      # Internationalization files
    └── bg/            # Bulgarian translations
```
## Dependencies
The application relies on the following key Python packages:
- Flask 3.1.1
- Flask-Babel 4.0.0
- Flask-WTF 1.2.2
- python-dotenv 1.1.0
- sib-api-v3-sdk 7.6.0 (Brevo API)
- gunicorn 23.0.0


## Email Templates
The application sends two types of emails:
1. **Confirmation to User**: Confirms that their request has been received
2. **Notification to Admin**: Details of the user's NAS requirements

Both emails are sent in the user's selected language (English or Bulgarian).
## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
## Acknowledgements
- [Flask](https://flask.palletsprojects.com/)
- [Flask-Babel](https://python-babel.github.io/flask-babel/)
- [Flask-WTF](https://flask-wtf.readthedocs.io/)
- [Brevo](https://www.brevo.com/) (formerly Sendinblue)
- [Docker](https://www.docker.com/)
