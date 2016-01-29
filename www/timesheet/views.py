# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from wtforms.ext.sqlalchemy.orm import model_form

from www.extensions import login_manager, db
from www.public.forms import LoginForm
from www.timesheet.forms import TimesheetForm
from www.timesheet.models import Timesheet
from www.user.forms import RegisterForm
from www.user.models import User
from www.utils import flash_errors

blueprint = Blueprint('timesheet', __name__, url_prefix='/timesheets', static_folder='../static')

@blueprint.route('/', methods=['GET'])
@login_required
def index():
    """List timesheet."""
    timesheets = Timesheet.query.all()
    return render_template('timesheets/timesheet_index.html', timesheets=timesheets)

@blueprint.route('/new', methods=['GET'])
@login_required
def new():
    form = TimesheetForm(request.form)
    return render_template('timesheets/timesheet_create.html', form=form)

@blueprint.route('/', methods=['POST'])
@login_required
def create():
    form = TimesheetForm(request.form)
    if request.method=='POST' and form.validate():
        timesheet = Timesheet(title=form.title.data)
        timesheet.user_id = current_user.id
        db.session.add(timesheet)
        db.session.commit()
        flash('Your timesheet was created')
        return redirect(url_for('timesheet.index'))
    return render_template('timesheets/timesheet_create.html', form=form)

@blueprint.route('/<id>', methods=['GET'])
@login_required
def show(id):
    item = Timesheet.get_by_id(id)
    return render_template('timesheets/timesheet_detail.html', item=item)

@blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    form = model_form(Timesheet, TimesheetForm)
    timesheet = Timesheet.get_by_id(id)
    form = TimesheetForm(request.form, timesheet)

    if form.validate_on_submit():
        form.populate_obj(timesheet)
        timesheet.put()
        flash("timesheet updated")
        return redirect(url_for("timesheet.index"))
    return render_template("timesheets/timesheet_edit.html", form=form, timesheet=timesheet)

@blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    timesheet = Timesheet.query.get(id)
    timesheet.title = request.form['title']
    db.session.commit()
    flash("timesheet updated")
    return redirect(url_for('timesheet.index'))

@blueprint.route('/<id>/delete', methods=['GET'])
@login_required
def destroy(id):
    post = Timesheet.get_by_id(id)
    db.session.delete(post)
    db.session.commit()
    flash ('deleted')

    return redirect(url_for('timesheet.index'))