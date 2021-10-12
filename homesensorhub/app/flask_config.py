#!/usr/bin/env python3
import os


class FlaskConfig():
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1234'
