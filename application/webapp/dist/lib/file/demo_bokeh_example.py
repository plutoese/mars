from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.charts import Bar, output_file, show
from bokeh.sampledata.autompg import autompg as df
from webapp.dist.lib.file.class_Excel import Excel
import pandas as pd

mexcel = Excel('E:/gitwork/application/webapp/static/file/2016-01-08/c80e8748-b5f8-11e5-887a-f582ef2c4802.xlsx')
mdata = mexcel.read()
index = mdata.pop(0)
mdata = pd.DataFrame(mdata,columns=index)
print(index)
print(mdata)

plot = figure()
plot.circle([1,2], [3,4])

script, div = components(plot)
print(script)
print(div)

print(df)

p = Bar(mdata, 'city', values='PM25', title="Total MPG by CYL")

output_file("bar.html")

show(p)

script, div = components(p)
print(script)
print(div)
