"""Configurations of the Flask application and its routes."""
# !/usr/bin/env python3
import os
import flask


from flask import render_template, flash, redirect, url_for
from .forms import LoginForm, MQTTForm
from homesensorhub.utils.configuration import Configuration


class FlaskApp:
    """Configures the Flask application and its routes."""

    def __init__(self) -> None:
        self.__app = self.__create_app()
        self.__create_routes(self.__app)

        self.__mqtt_data = {}

    def run(self, host: str = "0.0.0.0") -> None:
        """Run the Flask application on the given host.

        Args:
            host (str, optional): Host of the Flask application. Defaults to "0.0.0.0".
        """
        self.__app.run(debug=False, host=host)

    def mqtt_data(self) -> dict:
        """The MQTT configuration data extracted from the Flask application MQTT form.

        Returns:
            dict: The configuration data for the MQTT module.
        """
        return self.__mqtt_data

    def __create_app(self) -> flask.Flask:
        app = flask.Flask(__name__, instance_relative_config=True)
        app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        )

        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        return app

    def __create_routes(self, app) -> None:
        @app.route('/')
        def start():
            return render_template('home.html')

        @app.route('/home', methods=['GET'])
        def home():
            user = {'username': 'Min'}
            return render_template('home.html', user=user)

        @app.route('/mqtt', methods=['GET', 'POST'])
        def mqtt():
            data = Configuration().section("mqtt")
            mqtt_form = MQTTForm(data=data)

            if mqtt_form.validate_on_submit():
                self.__configure_mqtt_data(mqtt_form)
                flash("Succesfully updated MQTT form.", category="info")
            else:
                flash("Could not update MQTT form.", category="error")

            return render_template('mqtt.html', title="mqtt", form=mqtt_form)

        @app.route('/login', methods=['GET', 'POST'])
        def login():
            form = LoginForm()

            if form.validate_on_submit():
                flash(f"Login requested for user {form.username.data},"
                      "remember_me={form.remember_me.data}")
                return redirect(url_for('home'))

            return render_template('login.html', title='Sign In', form=form)

    def __configure_mqtt_data(self, mqtt_form: MQTTForm) -> None:
        try:
            validated_port = int(mqtt_form.port.data)
        except ValueError:
            print("The port is not an integer. Abort.")
            #  send this message in the UI

        self.__mqtt_data = {
            'address': mqtt_form.address.data,
            'port': validated_port,
            'client_id': mqtt_form.client_id.data,
            'root_topic': mqtt_form.root_topic.data
        }
        for section, entry in self.__mqtt_data.items():
            Configuration().update_entry("mqtt", section, value=entry)


if __name__ == "__main__":
    flask_application = FlaskApp()
    flask_application.run()
