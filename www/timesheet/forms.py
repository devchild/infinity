# -*- coding: utf-8 -*-
"""Public forms."""
from datetime import date, timedelta, datetime

from flask_wtf import Form
from sqlalchemy import and_
from wtforms import PasswordField, StringField, IntegerField, SelectField, DecimalField, FieldList, FormField, \
    HiddenField

from www.timesheet.fields import DurationField
from www.timesheet.models import Timesheet, TimesheetEntry
from www.user.models import User
from www.utils import daterange

MONTHS = [("1", "Jan"),
          ("2", "Feb"),
          ("3", "Mar"),
          ("4", "Apr"),
          ("5", "May"),
          ("6", "Jun"),
          ("7", "Jul"),
          ("8", "Aug"),
          ("9", "Sep"),
          ("10", "Oct"),
          ("11", "Nov"),
          ("12", "Dec")]

class TimesheetEntryForm(Form):
    id       = HiddenField()
    day      = HiddenField()
    activity = HiddenField()
    duration = DurationField()

    @property
    def is_empty(self):
        return self.duration.data == '' or self.duration.data == None

    @property
    def is_new(self):
        return self.id.data == ''

    def populate_obj(self, obj):
        self.day.populate_obj(obj, "day")
        self.duration.populate_obj(obj, "duration")
        self.activity.populate_obj(obj, "activity")

class CreateTimesheetForm(Form):
    title   = StringField()
    year    = IntegerField('Year')
    month   = SelectField(choices=MONTHS)

class EditTimesheetForm(Form):
    entries = FieldList(FormField(TimesheetEntryForm))

    def get_activities(self):
        return ["Development", "Verlof"]

    def populate_form(self, obj):
        for day in obj.included_days:
            for activity in self.get_activities():
                entry = obj.entries.filter(and_(TimesheetEntry.activity == activity, TimesheetEntry.day == day.day)).first()
                if not entry:
                    self.entries.append_entry(TimesheetEntry( day=day.day, activity=activity ))

    def populate_obj(self, obj):
        obj.entries.delete()

        for entry in self.entries:
            if not entry.form.is_empty:
                entry_obj = obj.entries.filter(TimesheetEntry.id == entry.form.id.data).first()
                if not entry_obj:
                    entry_obj = TimesheetEntry()
                    obj.entries.append(entry_obj)
                entry.form.populate_obj(entry_obj)