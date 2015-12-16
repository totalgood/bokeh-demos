import numpy as np
from datetime import date

from bokeh.io import curdoc
from bokeh.models import (
    ColumnDataSource,
    DatetimeAxis,
    Line,
    LinearAxis,
    Plot,
    Range1d,
)
from django.core.exceptions import AppRegistryNotReady
from happiness.models import Employee

document = curdoc()

start_date = date(2015, 6, 1)
end_date = date(2015, 8, 31)

x_range = Range1d(start_date, end_date)
y_range = Range1d(0, 10)
plot = Plot(
    plot_height=400, plot_width=800,
    toolbar_location=None, responsive=True,
    x_range=x_range, y_range=y_range,
    outline_line_color=None,
)
plot.add_layout(LinearAxis(), 'left')
plot.add_layout(DatetimeAxis(axis_label=None), 'below')

employee_pk_source = ColumnDataSource(data=dict(employee_pk=[]), name='employee_pk_source')
source = ColumnDataSource(data=dict(x=[], y=[]))
plot.add_glyph(source, Line(x='x', y='y', line_width=3, line_alpha=0.6, line_color='magenta', line_cap='round'))


def update_data():
    # This is gross - see https://github.com/bokeh/bokeh/issues/3349
    employee_pk = document.get_model_by_name('employee_pk_source').data['employee_pk'][0]
    try:
        employee = Employee.objects.get(pk=employee_pk)
        new_data = dict(
            x=employee.get_happiness_dates(start_date, end_date),
            y=employee.get_happiness_values(start_date, end_date)
        )
        # I want to only do this update if new_data is different, but can't find out a clean way
        source.data = new_data
    except Employee.DoesNotExist:
        source.data = dict(x=[], y=[])
    except AppRegistryNotReady:
        # This sets up django the first time around
        print('Setting up django')
        import django
        django.setup()

document.add_root(plot)
document.add_root(employee_pk_source)
document.add_periodic_callback(update_data, 200)
