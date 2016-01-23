from bokeh.document import Document
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral9

from happiness.models import Employee
from .utils import make_plot, make_legend


class IndividualsPlot(object):

    def __init__(self, user):
        self.user = user
        self.sources = {}
        self.renderers = {}
        self.document = Document()
        self.legend = make_legend()
        self.document.add_root(self.make_individuals_plot())
        self.update_data()

    def make_individuals_plot(self):
        plot = make_plot()
        all_employees = list(Employee.objects.all())
        for employee in all_employees:
            self.sources[employee.pk] = ColumnDataSource(data=dict(x=[], y=[], line_color=[]))
            line = plot.line(x='x', y='y', line_width=2, line_cap='round', source=self.sources[employee.pk])
            self.renderers[employee.pk] = {}
            self.renderers[employee.pk]['renderer'] = line
            self.renderers[employee.pk]['name'] = employee.user.first_name
        plot.add_layout(self.legend)
        return plot

    def update_data(self):
        user = self.user
        if user and hasattr(user, 'team'):
            employees = user.team.employee_set.all()
            legends = {}
            new_data = {}
            for i, employee in enumerate(employees):
                dates, happiness = employee.get_dates_happiness()
                new_data[employee.pk] = dict(x=dates, y=happiness)
                line = self.renderers[employee.pk]['renderer']
                line.glyph.line_color = Spectral9[i]

                # Update the legend info
                l = {}
                l['name'] = self.renderers[employee.pk]['name']
                l['renderers'] = [line]
                legends[employee.pk] = l

            # Update legend before data (seems to render better)
            self.legend.legends = [(l['name'], l['renderers']) for _, l in legends.items()]
            for employee in employees:
                self.sources[employee.pk].data = new_data[employee.pk]
