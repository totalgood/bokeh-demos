from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral9
from django.core.exceptions import AppRegistryNotReady
from happiness.models import Employee

from viz.utils import make_plot, setup_django

document = curdoc()
employee_pk_source = ColumnDataSource(data=dict(employee_pk=[]), name='employee_pk_source')

source = ColumnDataSource(data=dict(xs=[], ys=[], colors=[]))

plot = make_plot()
plot.multi_line(xs='xs', ys='ys', line_width=1, line_alpha=0.6, line_color='colors', line_cap='round', source=source)


def update_data():
    employee_pk = document.get_model_by_name('employee_pk_source').data['employee_pk'][0]
    try:
        employee = Employee.objects.get(pk=employee_pk)
        teams = employee.teams.all()
        new_data = dict(xs=[], ys=[], colors=[])
        for i, team in enumerate(teams):
            dates, happiness = team.get_team_dates_happiness()
            new_data['xs'].append(dates)
            new_data['ys'].append(happiness)
            new_data['colors'].append(Spectral9[i])
        source.data = new_data
    except Employee.DoesNotExist:
        source.data = dict(xs=[], ys=[], colors=[])
    except AppRegistryNotReady:
        setup_django()

def update_data_once():
    update_data()

document.add_root(plot)
document.add_root(employee_pk_source)
document.add_timeout_callback(update_data_once, 100)
document.add_periodic_callback(update_data, 2000)
