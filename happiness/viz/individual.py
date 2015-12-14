from bokeh.io import curdoc
from bokeh.models import (
    ColumnDataSource, DataRange1d, DatetimeAxis, Line, LinearAxis, Plot, Range1d,
)

document = curdoc()

source = ColumnDataSource(data=dict(), name='source')
plot = Plot(
    plot_height=400, plot_width=800,
    toolbar_location=None, responsive=True,
    x_range=DataRange1d(), y_range=Range1d(0, 9)
)
plot.add_glyph(source, Line(x='x', y='y', line_width=3, line_alpha=0.6, line_color='pink'))

document.add_root(source)
document.add_root(plot)
