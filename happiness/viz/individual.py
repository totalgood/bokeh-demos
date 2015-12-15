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
from happiness.models import Employee

import django
django.setup()

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
plot.add_glyph(source, Line(x='x', y='y', line_width=3, line_alpha=0.6, line_color='magenta'))


def get_user_data(employee):
    h_set = employee.happiness_set.all()
    dates = h_set.values_list('date', flat=True)
    x = np.array(dates)
    happinesses = h_set.values_list('happiness', flat=True)
    y = np.array(happinesses)
    return dict(x=x, y=y)


def update_data():
    employee_pk = document.get_model_by_name('employee_pk_source').data['employee_pk'][0]  # This is gross!
    try:
        employee = Employee.objects.get(pk=employee_pk)
        source.data = get_user_data(employee)
    except Employee.DoesNotExist:
        pass

document.add_root(plot)
document.add_root(employee_pk_source)
document.add_periodic_callback(update_data, 2000)
