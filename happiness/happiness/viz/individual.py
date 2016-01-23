from bokeh.document import Document
from bokeh.models import ColumnDataSource

from .utils import make_plot


class IndividualPlot(object):

    def __init__(self, user):
        self.user = user
        self.source = ColumnDataSource(data=dict(x=[], y=[]))
        self.update_data()
        self.document = Document()
        self.document.add_root(self.make_individual_plot())

    def make_individual_plot(self):
        plot = make_plot()
        plot.plot_height = 200
        plot.y_range.end = 9
        self.line = plot.line(
            x='x', y='y',
            line_width=1, line_alpha=0.6, line_color='magenta', line_cap='round',
            source=self.source
        )
        return plot

    def update_data(self):
        user = self.user
        if user and hasattr(user, 'employee'):
            employee = user.employee
            dates, happiness = employee.get_dates_happiness()
            new_data = dict(x=dates, y=happiness)
            self.source.data = new_data
