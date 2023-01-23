"""Entrypoint for the flask application."""
from .flask_application import FlaskApp

flask_application = FlaskApp()
flask_application.run()
