from datetime import datetime
from bokeh.io import curdoc
from bokeh.models import (
    ColumnDataSource,
    DatetimeAxis,
    HoverTool,
    Line,
    LinearAxis,
    Plot,
    Range1d,
)

document = curdoc()

start_date = datetime(2015, 6, 1)
end_date = datetime(2015, 8, 31)

x_range = Range1d(start_date, end_date)
y_range = Range1d(0, 10)
plot = Plot(
    plot_height=400, plot_width=800,
    toolbar_location=None, responsive=True,
    x_range=x_range, y_range=y_range,
    outline_line_color=None,
)

plot.add_layout(LinearAxis(), 'left')
plot.add_layout(DatetimeAxis(axis_label=None), 'below')

source = ColumnDataSource(data=dict(x=[], y=[]), name='source')

# This will generate an error, but its ok, as we add data to the session
plot.add_glyph(source, Line(x='x', y='y', line_width=3, line_alpha=0.6, line_color='magenta'))

document.add_root(source)
document.add_root(plot)
