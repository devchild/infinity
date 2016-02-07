from datetime import datetime, timedelta

from dateutil.parser import parse
from wtforms import Field, StringField, widgets
from wtforms.compat import text_type


class DurationField(StringField):
    widget = widgets.TextInput()
    format = "%H:%M"

    def process_formdata(self, valuelist):
        self.data = None

        if valuelist:
            duration_val = valuelist[0]
            if (len(duration_val) > 3):
                hours, minutes = duration_val.split(':')

                tmp = timedelta(hours=int(hours), minutes=int(minutes), seconds=0)
                if (tmp.total_seconds() != 0):
                    self.data = tmp

    def strfdelta(self, tdelta, fmt):
        d = {"days": tdelta.days}
        d["hours"], rem = divmod(tdelta.seconds, 3600)
        d["minutes"], d["seconds"] = divmod(rem, 60)
        return fmt.format(**d)

    def _value(self):
        return self.strfdelta(self.data, "{hours}:{minutes:02d}") if self.data is not None else ''

