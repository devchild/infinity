# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from www.extensions import login_manager
from www.public.forms import LoginForm
from www.user.forms import RegisterForm
from www.user.models import User
from www.utils import flash_errors

blueprint = Blueprint('timesheet', __name__, url_prefix='/timesheets', static_folder='../static')

@blueprint.route('/', methods=['GET'])
@login_required
def index():
    """List timesheet."""
    return render_template('timesheets/timesheet_index.html')