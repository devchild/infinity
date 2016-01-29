# -*- coding: utf-8 -*-
"""Timesheet models."""
import datetime as dt

from www.database import Column, Model, SurrogatePK, db, reference_col, relationship

class Timesheet(SurrogatePK, Model):
    __tablename__ = 'timesheets'
    title = Column(db.String(255), unique=False, nullable=False)
    user_id = reference_col('users', nullable=False)
    user = relationship('User', backref='timesheets')

    def __init__(self, title, **kwargs):
        """Create instance."""
        db.Model.__init__(self, title=title, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return 'Timesheet({title})'.format(title=self.title)


class TimesheetEntry(SurrogatePK, Model):
    __tablename__ = 'timesheet_entries'
    timesheet_id = reference_col('timesheets', nullable=False)
    timesheet = relationship('Timesheet', backref='entries')

