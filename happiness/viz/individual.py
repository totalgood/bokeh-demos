from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from django.core.exceptions import AppRegistryNotReady
from django.contrib.auth.models import User

from viz.utils import make_plot, setup_django

document = curdoc()

# This source just holds the employee_id it doesn't which is then used to get the data for the plot.
# There will be a cleaner way of doing this in the future - see https://github.com/bokeh/bokeh/issues/3349
user_pk_source = ColumnDataSource(data=dict(user_pk=[]), name='user_pk_source')

source = ColumnDataSource(data=dict(x=[], y=[]))  # This is the empty data source that will drive the plot
plot = make_plot()
plot.plot_height = 200
plot.y_range.end = 9
plot.line(x='x', y='y', line_width=1, line_alpha=0.6, line_color='magenta', line_cap='round', source=source)


def update_data():
    user_pk = document.get_model_by_name('user_pk_source').data['user_pk'][0]
    try:
        employee = User.objects.get(pk=user_pk).employee
        dates, happiness = employee.get_dates_happiness()
        new_data = dict(x=dates, y=happiness)
        source.data = new_data
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
