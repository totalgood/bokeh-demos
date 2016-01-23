from bokeh.client import pull_session
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral4

from .utils import make_plot, make_legend


def update_team_data(user, bokeh_session_id):
    session = pull_session(session_id=bokeh_session_id)
    teams = user.employee.teams.all()
    for team in teams:
        dates, happiness = team.get_team_dates_happiness()
        source = session.document.select_one(
            {'type': ColumnDataSource,
             'name': team.name}
        )
        source.data = dict(x=dates, y=happiness)


def make_team_plot(user):
    plot = make_plot()
    legends = []
    teams = user.employee.teams.all()
    for i, team in enumerate(teams):
        dates, happiness = team.get_team_dates_happiness()
        source = ColumnDataSource(data=dict(x=dates, y=happiness), name=team.name)
        line = plot.line(x='x', y='y', line_width=2, line_color=Spectral4[i], line_cap='round', source=source)
        legends.append((team.name, [line]))
    plot.add_layout(make_legend(legends=legends))
    return plot
