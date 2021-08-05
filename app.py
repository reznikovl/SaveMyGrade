import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import random

import numpy as np
import pandas as pd

from savemygrade import *


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id="dropdown1",
        options=[{'label': 'True', 'value': 'True'}, {'label': 'False', 'value': 'False'}],
        value='True',
        clearable=False,
    ),
    # dcc.Dropdown(
    #     id="dropdown2",
    #     options=[{"label": "Option " + str(x), "value": x} for x in range(1001, 2000)],
    #     value=1001,
    #     clearable=False,
    # ),
    dcc.Graph(id="bar-chart"),
])

@app.callback(
    Output("bar-chart", "figure"),
    [Input("dropdown1", "value")]
)


def update_bar_chart(day):
    # mask = df["day"] == day
    # fig = px.bar(df[mask], x="sex", y="total_bill", 
    #              color="smoker", barmode="group")
    # return fig
    # return f"From form 1: {day1}, and from form 2: {day2}"
    # app.logger.info(plot(course='MATH 8', quarter='Fall 2020', percentage=False, professors=[]))
    app.logger.info('in update graph')
    show_percent = True if day == 'True' else False
    return plot(course='MATH 8', quarter='Fall 2020', percentage=show_percent, professors=[])

app.run_server(debug=True)