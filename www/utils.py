# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from datetime import timedelta, datetime

from flask import flash


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def getmonday(dt):
    return dt - datetime.timedelta(days=dt.weekday())

def getsunday(dt):
    return getmonday(dt) + datetime.timedelta(days=6)

#start_date = date(2013, 1, 1)
#end_date = date(2015, 6, 2)
#for single_date in daterange(start_date, end_date):
#    print(single_date.strftime("%Y-%m-%d"))
