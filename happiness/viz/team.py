from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral4
from django.core.exceptions import AppRegistryNotReady

from happiness.models import Employee, Team
from viz.utils import make_plot, make_legend, setup_django

document = curdoc()

employee_pk_source = ColumnDataSource(data=dict(employee_pk=[]), name='employee_pk_source')
sources = {}
renderers = {}

plot = make_plot()
legend = make_legend()
team_list = list(Team.objects.all())
for i, team in enumerate(team_list):
    sources[team.name] = ColumnDataSource(data=dict(x=[], y=[]))
    line = plot.line(x='x', y='y', line_width=2, line_color=Spectral4[i], line_cap='round', source=sources[team.name])
    renderers[team.name] = line
plot.add_layout(legend)


def update_data():
    employee_pk = document.get_model_by_name('employee_pk_source').data['employee_pk'][0]
    try:
        employee = Employee.objects.get(pk=employee_pk)
        teams = employee.teams.all()
        new_data = dict(x=[], y=[], colors=[])
        legends = {}
        for team in teams:
            dates, happiness = team.get_team_dates_happiness()
            new_data = dict(x=dates, y=happiness)
            sources[team.name].data = new_data
            legends[team.name] = renderers[team.name]
        legend.legends = [(k, [v]) for k, v in legends.items()]

    except Employee.DoesNotExist:
        pass
    except AppRegistryNotReady:
        setup_django()


def update_data_once():
    update_data()

document.add_root(plot)
document.add_root(employee_pk_source)
document.add_timeout_callback(update_data_once, 100)
document.add_periodic_callback(update_data, 2000)
