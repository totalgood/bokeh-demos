from bokeh.plotting import Figure
from bokeh.models import Range1d


def make_plot():
    plot = Figure(
        plot_height=400,
        plot_width=800,
        responsive=True,
        tools="xpan,xwheel_zoom,xbox_zoom,reset",
        x_axis_type='datetime'
    )
    plot.x_range.follow = "end"
    plot.x_range.follow_interval = 120 * 24 * 60 * 60 * 1000
    plot.x_range.range_padding = 0
    plot.y_range = Range1d(0, 9)
    return plot


def setup_django():
    print('Setting up django')
    import django
    django.setup()
