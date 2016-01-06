from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral9
from django.core.exceptions import AppRegistryNotReady
from django.contrib.auth.models import User

from happiness.models import Employee
from viz.utils import make_plot, make_legend, setup_django

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
    renderers[employee.pk] = line
plot.add_layout(legend)


def update_data():
    user_pk = document.get_model_by_name('user_pk_source').data['user_pk'][0]
    try:
        manager = User.objects.get(pk=user_pk)
        employees = manager.team.employee_set.all()
        legends = {}
        for i, employee in enumerate(employees):
            dates, happiness = employee.get_dates_happiness()
            new_data = dict(x=dates, y=happiness)
            sources[employee.pk].data = new_data
            line = renderers[employee.pk]
            line.line_color = Spectral9[i]
            legends[employee.pk] = line
        legend.legends = [(k, [v]) for k, v in legends.items()]

    except User.DoesNotExist:
        pass
    except AppRegistryNotReady:
        setup_django()


def update_data_once():
    update_data()

document.add_root(plot)
document.add_root(user_pk_source)
document.add_timeout_callback(update_data_once, 100)
document.add_periodic_callback(update_data, 2000)
