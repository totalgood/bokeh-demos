from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral9

from happiness.models import Employee
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
all_employees = list(Employee.objects.all())
for employee in all_employees:
    sources[employee.pk] = ColumnDataSource(data=dict(x=[], y=[], line_color=[]))
    line = plot.line(x='x', y='y', line_width=2, line_cap='round', source=sources[employee.pk])
    renderers[employee.pk] = {}
    renderers[employee.pk]['renderer'] = line
    renderers[employee.pk]['name'] = employee.user.first_name
plot.add_layout(legend)


def update_data():
    user = get_user(document)
    if user and hasattr(user, 'team'):
        employees = user.team.employee_set.all()
        legends = {}
        new_data = {}
        for i, employee in enumerate(employees):
            dates, happiness = employee.get_dates_happiness()
            new_data[employee.pk] = dict(x=dates, y=happiness)
            line = renderers[employee.pk]['renderer']
            line.glyph.line_color = Spectral9[i]

            # Update the legend info
            l = {}
            l['name'] = renderers[employee.pk]['name']
            l['renderers'] = [line]
            legends[employee.pk] = l

        # Update legend before data (seems to render better)
        legend.legends = [(l['name'], l['renderers']) for _, l in legends.items()]
        for employee in employees:
            sources[employee.pk].data = new_data[employee.pk]


def update_data_once():
    update_data()

document.add_root(plot)
document.add_root(user_pk_source)
document.add_timeout_callback(update_data_once, 250)
document.add_periodic_callback(update_data, 5000)
