#!/usr/bin/env python3
from flask import render_template, flash, redirect, url_for
from forms import LoginForm, MQTTForm
from flask import Flask
import os

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
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
    @app.route('/')

    @app.route('/home', methods=['GET'])
    def home():
        user = {'username': 'Min'}
        return render_template('home.html', user=user)

    @app.route('/mqtt', methods=['GET', 'POST'])
    def mqtt():
        mqtt_form = MQTTForm()
        return render_template('mqtt.html', title="mqtt", form=mqtt_form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()

        if form.validate_on_submit():
            flash('Login requested for user {}, remember_me={}'.
                  format(form.username.data, form.remember_me.data))
            return redirect(url_for('home'))

        return render_template('login.html', title='Sign In', form=form)


if __name__ == "__main__":
    app = create_app()
    create_routes(app)
    app.run(debug=True, host="0.0.0.0")
