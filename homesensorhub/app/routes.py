"""Configurations of the Flask application and its routes."""
# !/usr/bin/env python3
import os
import flask


from flask import render_template, flash, redirect, url_for
from .forms import LoginForm, MQTTForm


def create_app(test_config=None):
    """Configure the Flask application."""
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


def create_routes(app) -> None:
    """Create the Flask application URL routes."""

    @app.route('/home', methods=['GET'])
    def home():
        user = {'username': 'Min'}
        return render_template('home.html', user=user)

    @app.route('/mqtt', methods=['GET', 'POST'])
    def mqtt():
        print(flask.request.method)
        mqtt_form = MQTTForm()

        if mqtt_form.validate_on_submit():
            address = mqtt_form.address.data
            port = mqtt_form.port.data
            client_id = mqtt_form.client_id.data
            root_topic = mqtt_form.root_topic.data
            print("Address: " + address, port, client_id, root_topic)

        return render_template('mqtt.html', title="mqtt", form=mqtt_form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()

        if form.validate_on_submit():
            flash(f"Login requested for user {form.username.data},"
                  "remember_me={form.remember_me.data}")
            return redirect(url_for('home'))

        return render_template('login.html', title='Sign In', form=form)


if __name__ == "__main__":
    flask_application = create_app()
    create_routes(flask_application)
    flask_application.run(debug=True, host="0.0.0.0")
