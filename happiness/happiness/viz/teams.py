from bokeh.document import Document
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral4

from .utils import make_plot


class TeamsPlot(object):

    def __init__(self, user):
        self.user = user
        self.source = ColumnDataSource(data=dict(x=[], y=[]))
        self.update_data()
        self.document = Document()
        self.document.add_root(self.make_teams_plot())

    def make_teams_plot(self):
        plot = make_plot()
        plot.plot_height = 200
        plot.y_range.end = 9
        plot.line(
            x='x', y='y',
            line_width=2, line_color=Spectral4[3], line_cap='round',
            source=self.source
        )
        return plot

    def update_data(self):
        user = self.user
        if user and hasattr(user, 'team'):
            team = user.team
            dates, happiness = team.get_team_dates_happiness()
            new_data = dict(x=dates, y=happiness)
            self.source.data = new_data
