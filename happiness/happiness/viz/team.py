from bokeh.document import Document
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral4

from happiness.models import Team
from .utils import make_plot, make_legend


class TeamPlot(object):

    def __init__(self, user):
        self.user = user
        self.sources = {}
        self.renderers = {}
        self.document = Document()
        self.legend = make_legend()
        self.document.add_root(self.make_team_plot())
        self.update_data()

    def make_team_plot(self):
        plot = make_plot()
        team_list = list(Team.objects.all())
        for i, team in enumerate(team_list):
            self.sources[team.name] = ColumnDataSource(data=dict(x=[], y=[]))
            line = plot.line(x='x', y='y', line_width=2, line_color=Spectral4[i], line_cap='round', source=self.sources[team.name])
            self.renderers[team.name] = line
        plot.add_layout(self.legend)
        return plot

    def update_data(self):
        user = self.user
        if user and hasattr(user, 'employee'):
            employee = user.employee
            teams = employee.teams.all()
            legends = {}
            new_data = {}
            for team in teams:
                dates, happiness = team.get_team_dates_happiness()
                new_data[team.name] = dict(x=dates, y=happiness)
                legends[team.name] = self.renderers[team.name]

            # Update legend before data (seems to render better)
            self.legend.legends = [(k, [v]) for k, v in legends.items()]
            for team in teams:
                self.sources[team.name].data = new_data[team.name]
