#!/usr/bin/env python3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, HostnameValidation
from flask import request

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class MQTTForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    port = StringField('Port', validators=[DataRequired()])
    client_id = StringField('Client ID')
    root_topic = StringField('Root Topic', validators=[DataRequired()])
    submit = SubmitField('Sign In')
