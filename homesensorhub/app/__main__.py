"""Entrypoint for the flask application."""
from .routes import create_app, create_routes

flask_application = create_app()
create_routes(flask_application)
flask_application.run(debug=True, host="0.0.0.0")
