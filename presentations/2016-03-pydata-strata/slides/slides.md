# Intro to data visualization with Bokeh

## PyData at Strata

- Sarah Bird [@birdsarah](https://twitter.com/birdsarah)
- Bryan Van de Ven [@bryvdv](https://twitter.com/bryvdv)

http://github.com/bokeh/bokeh-demos/

<small>March 29th, 2016</small>


---

## Overview

- 11:30 - 12:30 Intro to Bokeh ecosystem (code-along)
- 12:30 - 13:30 LUNCH
- 13:30 - 14:30 Hands-on examples (tutorials or bring your own data)

---


## Bokeh

<img class="slide_image" src="images/gallery-screenshot.png" style="position: absolute; top: 0; right: 0;">

- data visualization
- web-based & interactive
- no javascript required
- large data
- streaming data


---

## Core concepts for today

- Overview of Bokeh's functionality
- Navigating Bokeh's interfaces 
 - charts, plotting, and probably not models!
- Bokeh server 
 - what it is, what it isn't, do I need it
- Sharing your work 
 - notebook, standalone files, server 
- Awareness of the Bokeh ecosystem

---
<img class="slide_image" src="images/box_chart.png" style="position: absolute; top: -20px; right: 0; width: 200px; height: 200px">
### Demo 1 - Charts in the notebook
quick & easy data exploration

* work in the notebok
```python
from bokeh.io import output_notebook, show
output_notebook()
```
* make charts - simple one-liners accept tabular data
```python
from bokeh.charts import Bar, BoxPlot, Histogram, Scatter....
Scatter(df, x='mpg', y='hp', color='cyl')
BoxPlot(df, values='mpg', label='cyl', marker='square')
```

<small>
[bokeh.pydata.org/en/latest/docs/user_guide/charts.html](http://bokeh.pydata.org/en/latest/docs/user_guide/charts.html)
</small>
---
<img class="slide_image" src="images/clustering.png" style="position: absolute; top: -50px; right: -50px; width: 400px; height: 200px">
### Demo 2 - Server - clustering
interact in the browser, run by python code
```python
def update_samples_or_dataset(attrname, old, new):
    dataset = dataset_select.value
    algorithm = algorithm_select.value
    X, y = get_dataset(dataset, n_samples)
    X, y_pred = clustering(X, algorithm, n_clusters)
    source.data['x'] = X[:, 0]
    source.data['y'] = X[:, 1]
    
algorithm_select = Select(value='MiniBatchKMeans', options=opts)
algorithm_select.on_change('value', update_algorithm_or_clusters)
```

<small>
[github.com/bokeh/bokeh/tree/master/examples/app/clustering](https://github.com/bokeh/bokeh/tree/master/examples/app/clustering)
</small>
---

### Demo 3 - Server - streaming
<img class="slide_image" src="images/ohlc.png" style="position: absolute; top: 0px; right: 0px; width: 400px; height: 250px">

connect your plot to a streaming <br />
data source

bokeh will take care of the rest


```python
def update():
    new_data = get_new_data()
    source.stream(new_data, 300)
    
doc.add_periodic_callback(update, 50)
```
<small>
[github.com/bokeh/bokeh/tree/master/examples/app/ohlc](https://github.com/bokeh/bokeh/tree/master/examples/app/ohlc)
</small>
---
<img class="slide_image" src="images/datashader.png" style="position: absolute; top: 0px; right: 0px; width: 300px; height: 3 00px">
### Demo 4 - Datashader
Plotting **very** large datasets meaningfully

Uses bokeh's interactivity, hooks into <br />
powerful python libraries

[datashader.readthedocs.org](http://datashader.readthedocs.org)

---

## Core concepts for today

- Overview of Bokeh's functionality
- Navigating Bokeh's interfaces 
 - charts, plotting, and probably not models!
- Bokeh server 
 - what it is, what it isn't, do I need it
- Sharing your work 
 - notebook, standalone files, server 
- Awareness of the Bokeh ecosystem

---

## Bokeh - Core

- Python-based - http://bokeh.pydata.org
- Charts (Bar chart, Histogram...)
- Custom plots
- User interactions & styling
- Server interactions

---

## Bokeh - Ecosystem

- Other language bindings: rbokeh (actively maintained), scala (activeley maintained), julia (not maintained), typescript (coming soon)
- Datashader - interact with BIG<sup>**</sup> data
- Write your own custom models

---

## Interfaces

There are a number of ways to use Bokeh - pick the one that's right for you:

* Charts (high speed)
* Plotting (sensible defaults)
* Models (high customization)

We'll come back to this multiple times today.

---

<h5 style="padding-top: 1em; margin-bottom: -0.2em"> `bokeh.charts` (high speed)</h5>

- One-line charts
- Processes your data & spits out a chart


<h5 style="padding-top: 1em; margin-bottom: -0.2em"> `bokeh.plotting` (sensible defaults)</h5>

- Tries to pick sensible defaults
- You organize your data, it organizes your plot

<h5 style="padding-top: 1em; margin-bottom: -0.2em"> `bokeh.models` (high customization)</h5>

- The lowest level
- Offers you the most control
- Do all the work yourself

---

## Interfaces

* Charts (high speed)
* Plotting (sensible defaults)
* Models (high customization)

We'll come back to this multiple times today.

---

# Charts

---

#### Charts

---

# Plotting

---

#### Plotting


---

### Output

* output_notebook
* output_file
* embedding - file_html, components

---

### Resources

* `INLINE` - in the file
* `CDN` - load from web
* There are oter options

---

# Server

---

## Bokeh Server

- deep interactivity
- streaming data

---
## Getting set-up

- In order of simplicity:
 - Anaconda https://www.continuum.io/downloads
 - **Miniconda http://conda.pydata.org/miniconda.html (my personal preference)**
   
    `conda install bokeh`

 - Pip (can take a long time due to dependencies)

      `pip install bokeh`

***You don't need to do this now, we will be available to help duing lunch, so you're ready for the tutorials***

---

# Appendix

* compat
* user & reference guide
* search
* examples

---

## Hacker-slides how-to

- Separate slides using '`---`' on a blank line
- Write github flavored markdown
- Click 'Present' (top right) when you're ready to talk
- There is also a speaker view, with notes - press '`s`'
- Press '`?`' with focus on the presentation for shortcuts
- <em>You can use html when necessary</em>
- Share the 'Present' URL with anyone you like!

Learn more:
- [RevealJS Demo/Manual](http://lab.hakim.se/reveal-js)
- [RevealJS Project/README](https://github.com/hakimel/reveal.js)
- [GitHub Flavored Markdown](https://help.github.com/articles/github-flavored-markdown)

Note:
- Anything after `Note:` will only appear here
