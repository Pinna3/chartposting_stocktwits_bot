import plotly.graph_objs as go
import random
from statistics import stdev, mean

# a = [x**2 for x in range(20)]
a = [random.randint(-100, 300) for x in range(500)]
b = [x for x in range(500)]
s = [round(stdev(a), 1) for x in range(500)]
m = [round(mean(a), 1) for x in range(500)]
stdl = [(round(mean(a), 1)-round(stdev(a), 1)) for x in range(500)]
stdu = [(round(mean(a), 1)+round(stdev(a), 1)) for x in range(500)]


test = {'x': b, 'y': a, 'type': 'scatter', 'mode': 'lines',
    'line': {'width': 1, 'color': 'blue'}, 'name': 'RNDM'}

mean = {'x': b, 'y': m, 'type': 'scatter', 'mode': 'lines',
    'line': {'width': 1, 'color': 'green'}, 'name': 'STD'}

std_lower = {'x': b, 'y': stdl, 'type': 'scatter', 'mode': 'lines',
    'line': {'width': 1, 'color': 'red'}, 'name': 'STD'}

std_upper = {'x': b, 'y': stdu, 'type': 'scatter', 'mode': 'lines',
    'line': {'width': 1, 'color': 'red'}, 'name': 'STD'}


data = [test, mean, std_lower, std_upper]
layout = go.Layout({'title': {'text': 'STD DEV TEST',
        'font': {'size': 15}}})
fig = go.Figure(data=data, layout=layout)
# fig.write_html("Microsoft(MSFT) Moving Averages.html")
fig.show()
