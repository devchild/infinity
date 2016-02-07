# -*- coding: utf-8 -*-
"""Timesheet models."""
import datetime as dt
from calendar import monthrange

from sqlalchemy import Interval
from sqlalchemy.orm import backref

from www.database import Column, Model, SurrogatePK, db, reference_col, relationship
from www.utils import daterange


class Timesheet(SurrogatePK, Model):
    __tablename__ = 'timesheets'
    title = Column(db.String(255), unique=False, nullable=False)
    user_id = reference_col('users', nullable=False)
    user = relationship('User', backref='timesheets')

    year = Column(db.SmallInteger(), nullable=False)
    month = Column(db.SmallInteger(), nullable=False)

    @property
    def timesheet_start(self):
        return dt.datetime(year=self.year, month=self.month, day=1)

    @property
    def timesheet_end(self):
        last_day_of_month = monthrange(self.year, self.month)[1]
        return dt.datetime(year=self.year, month=self.month, day=last_day_of_month)

    @property
    def included_days(self):
        return [day for day in daterange(self.timesheet_start, self.timesheet_end)]

    def __init__(self, title, **kwargs):
        """Create instance."""
        db.Model.__init__(self, title=title, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return 'Timesheet({title})'.format(title=self.title)

class TimesheetEntry(SurrogatePK, Model):
    __tablename__ = 'timesheet_entries'
    timesheet_id = reference_col('timesheets', nullable=False)
    timesheet = relationship('Timesheet', backref=backref('entries', lazy='dynamic', cascade="all, delete-orphan"))

    day = db.Column(db.SmallInteger(), nullable=False)
    duration = db.Column(Interval, nullable=False)
    activity = db.Column(db.String(255), nullable=False)

