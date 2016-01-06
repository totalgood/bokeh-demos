from bokeh.io import curdoc
from bokeh.models import (
    ColumnDataSource,
    Line,
    Range1d,
)
from bokeh.plotting import Figure
from django.core.exceptions import AppRegistryNotReady
from happiness.models import Employee

document = curdoc()
employee_pk_source = ColumnDataSource(data=dict(employee_pk=[]), name='employee_pk_source')

plot = Figure(
    plot_height=400,
    plot_width=800,
    responsive=True,
    tools="xpan,xwheel_zoom,xbox_zoom,reset",
    x_axis_type='datetime'
)
plot.x_range.follow = "end"
plot.x_range.follow_interval = 120 * 24 * 60 * 60 * 1000
plot.x_range.range_padding = 0
plot.y_range = Range1d(0, 10)

source = ColumnDataSource(data=dict(x=[], y=[]))
plot.add_glyph(source, Line(x='x', y='y', line_width=1, line_alpha=0.6, line_color='magenta', line_cap='round'))


def update_data():
    # This could be better - see https://github.com/bokeh/bokeh/issues/3349
    employee_pk = document.get_model_by_name('employee_pk_source').data['employee_pk'][0]
    try:
        employee = Employee.objects.get(pk=employee_pk)
        new_data = dict(
            x=employee.get_happiness_dates(),
            y=employee.get_happiness_values()
        )
        # Would like a way to do this update if new_data is different.
        source.data = new_data
    except Employee.DoesNotExist:
        source.data = dict(x=[], y=[])
    except AppRegistryNotReady:
        print('Setting up django')
        import django
        django.setup()

document.add_root(plot)
document.add_root(employee_pk_source)
document.add_periodic_callback(update_data, 200)
