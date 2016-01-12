from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral4

from happiness.models import Team
from viz.utils import make_plot, make_legend, get_user, django_setup

if not django_setup:
    import django
    django.setup()
    django_setup = True

document = curdoc()

user_pk_source = ColumnDataSource(data=dict(user_pk=[]), name='user_pk_source')
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
    user = get_user(document)
    if user and hasattr(user, 'employee'):
        employee = user.employee
        teams = employee.teams.all()
        legends = {}
        new_data = {}
        for team in teams:
            dates, happiness = team.get_team_dates_happiness()
            new_data[team.name] = dict(x=dates, y=happiness)
            legends[team.name] = renderers[team.name]

        # Update legend before data (seems to render better)
        legend.legends = [(k, [v]) for k, v in legends.items()]
        for team in teams:
            sources[team.name].data = new_data[team.name]


def update_data_once():
    update_data()

document.add_root(plot)
document.add_root(user_pk_source)
document.add_timeout_callback(update_data_once, 250)
document.add_periodic_callback(update_data, 5000)
