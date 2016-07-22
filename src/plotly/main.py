import pandas as pd
import numpy as np
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.graph_objs as go
import random
from plotly import tools

# delete all vars in python shell
# for name in dir():
#     if not name.startswith('_'):
#         del globals()[name]
df1 = pd.read_csv('messages.csv', index_col='id')
df2 = pd.read_csv('streams.csv')
# plot bubblechart, messages per stream
slice = df1['stream_id'].value_counts(normalize=False, sort=True, ascending=False, bins=None, dropna=True)

df_slice = slice.to_frame('df_slice')
df_slice['stream_id'] = df_slice.index
df_slice = pd.merge(df_slice, df2, on='stream_id', how='inner')
trace = go.Scatter(
    x = random.sample(xrange(df_slice.shape[0]), df_slice.shape[0]),
    y = df_slice['df_slice'].values,
    text=df_slice['stream_name'],
    mode = 'markers',
    marker=dict(
        size=df_slice['df_slice'].values/6500
    ),
    name='Size'
)
layout = go.Layout(
    title='Total Messages Sent Per Stream',
    xaxis=dict(
        title='',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='# Of Messages Axis',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
)
data = [trace]
fig = go.Figure(data=data, layout=layout)

plot_url = py.plot(fig, filename='basic_bubblechat-size')


# stacked area chart with cumulative values

# bar chart line with plot
# df1 = pd.read_csv('messages.csv', index_col='id')
slice = df1['message'].value_counts(normalize=False, sort=True, ascending=True, bins=None, dropna=True)
y_percentage = slice.tail(10).values/float(df1.shape[0]) * 100
y_count = slice.tail(10).values
x_labels = slice.tail(10).index


trace0 = go.Bar(
    x=y_percentage,
    y=x_labels,
    marker=dict(
        color='rgba(50, 171, 96, 0.6)',
        line=dict(
            color='rgba(50, 171, 96, 1.0)',
            width=1),
    ),
    name='Percentage of all messages sent',
    orientation='h',
)
trace1 = go.Scatter(
    x=y_count,
    y=x_labels,
    mode='lines+markers',
    line=dict(
        color='rgb(128, 0, 128)'),
    name='Raw messages sent',
)
layout = dict(
    title='Top 10 Most Significant Memes',
    yaxis1=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        domain=[0, 0.85],
    ),
    yaxis2=dict(
        showgrid=False,
        showline=True,
        showticklabels=False,
        linecolor='rgba(102, 102, 102, 0.8)',
        linewidth=2,
        domain=[0, 0.85],
    ),
    xaxis1=dict(
        zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=True,
        domain=[0, 0.42],
    ),
    xaxis2=dict(
        zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=True,
        domain=[0.47, 1],
        side='top',
        dtick=25000,
    ),
    legend=dict(
        x=0.029,
        y=1.038,
        font=dict(
            size=10,
        ),
    ),
    margin=dict(
        l=100,
        r=20,
        t=70,
        b=70,
    ),
    paper_bgcolor='rgb(248, 248, 255)',
    plot_bgcolor='rgb(248, 248, 255)',
)

annotations = []

y_s = np.round(y_percentage, decimals=2)
y_nw = np.rint(y_count)

# Adding labels
for ydn, yd, xd in zip(y_nw, y_s, x_labels):
    # labeling the scatter savings
    annotations.append(dict(xref='x2', yref='y2',
                            y=xd, x=ydn - 20000,
                            text='{:,}'.format(ydn) + '',
                            font=dict(family='Arial', size=12,
                                      color='rgb(128, 0, 128)'),
                            showarrow=False))
    # labeling the bar net worth
    annotations.append(dict(xref='x1', yref='y1',
                            y=xd, x=yd + 3,
                            text=str(yd) + '%',
                            font=dict(family='Arial', size=12,
                                      color='rgb(50, 171, 96)'),
                            showarrow=False))
# Source
annotations.append(dict(xref='paper', yref='paper',
                        x=-0.2, y=-0.109,
                        text=
                             '(2016), Data collected over period of 4 days. ' +
                             'Most spammed messages. Notably, a CapCom tournament was played with 150k during its showing. ',
                        font=dict(family='Arial', size=10,
                                  color='rgb(150,150,150)'),
                        showarrow=False))

layout['annotations'] = annotations

# Creating two subplots
fig = tools.make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                          shared_yaxes=False, vertical_spacing=0.001)

fig.append_trace(trace0, 1, 1)
fig.append_trace(trace1, 1, 2)

fig['layout'].update(layout)
py.plot(fig, filename='significant_memes')