"""Forms classes for various Flask sub-pages."""
# !/usr/bin/env python3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Form defining the necessary fields for log-in."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class MQTTForm(FlaskForm):
    """Form defining the necessary fields for the MQTT bus configuration."""
    address = StringField('Address', validators=[DataRequired()])
    port = StringField('Port', validators=[DataRequired()])
    client_id = StringField('Client ID')
    root_topic = StringField('Root Topic', validators=[DataRequired()])
    submit = SubmitField('Save')
