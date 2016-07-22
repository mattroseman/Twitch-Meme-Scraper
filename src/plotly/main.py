import pandas as pd
import numpy as np
import plotly.plotly as py
from plotly.graph_objs import *

df = pd.read_csv('messages.csv')
list = df['stream_id'].value_counts(normalize=False, sort=True, ascending=False, bins=None, dropna=True)

# trace0 = Scatter(
            # x=[1, 2, 3, 4],
                # y=[10, 15, 13, 17]
                # )
# trace1 = Scatter(
            # x=[1, 2, 3, 4],
                # y=[16, 5, 11, 9]
                # )
# data = Data([trace0, trace1])

# py.iplot(data, filename = 'basic-line')



