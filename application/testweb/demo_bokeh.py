from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.charts import Bar, output_file, show
from bokeh.sampledata.autompg import autompg as df

plot = figure()
plot.circle([1,2], [3,4])

script, div = components(plot)
print(script)
print(div)

print(df)
p = Bar(df, 'cyl', values='mpg', title="Total MPG by CYL")

output_file("bar.html")

show(p)