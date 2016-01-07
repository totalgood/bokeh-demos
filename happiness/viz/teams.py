from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral4

from viz.utils import make_plot, get_user, django_setup

if not django_setup:
    import django
    django.setup()
    django_setup = True
document = curdoc()

user_pk_source = ColumnDataSource(data=dict(user_pk=[]), name='user_pk_source')
sources = {}
renderers = {}

source = ColumnDataSource(data=dict(x=[], y=[]))
plot = make_plot()
plot.plot_height = 200
plot.y_range.end = 9
plot.line(x='x', y='y', line_width=2, line_color=Spectral4[3], line_cap='round', source=source)


def update_data():
    user = get_user(document)
    if user and hasattr(user, 'team'):
        team = user.team
        dates, happiness = team.get_team_dates_happiness()
        new_data = dict(x=dates, y=happiness)
        source.data = new_data


def update_data_once():
    update_data()


document.add_root(plot)
document.add_root(user_pk_source)
document.add_timeout_callback(update_data_once, 250)
document.add_periodic_callback(update_data, 5000)
