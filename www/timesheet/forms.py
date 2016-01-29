# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired

from www.timesheet.models import Timesheet
from www.user.models import User

class TimesheetForm(Form):
    title = StringField('title', validators=[DataRequired()])
