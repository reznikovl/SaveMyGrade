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

dropdown_width='60%'

app.layout = html.Div([
    html.Center(html.H1('Let\'s Save Your Grade!')),
    'Quarter',
    dcc.Dropdown(
        id="quarter_dropdown",
        options=[{"label": x, "value": x} for x in reversed(get_quarters())],
        value='Winter 2020',
        style={'width': dropdown_width},
        clearable=False
    ),
    html.Br(),
    'Course',

    dcc.Dropdown(
        id="class_dropdown",
        style={'width': dropdown_width},
        clearable=False,
    ),

    html.Br(),
    'Display Options',

    dcc.Dropdown(
        id="percent_dropdown",
        options=[{'label': 'Show Percentage of Students', 'value': 'True'}, {'label': 'Show Number of Students', 'value': 'False'}],
        value='True',
        style={'width': dropdown_width},
        clearable=False,
    ),

    html.Br(),
    'Professors:',
    dcc.Checklist(
        id="professor_checklist"
    ),
    dcc.Graph(id="bar-chart"),
])

@app.callback(
    Output('class_dropdown', 'options'),
    Input('quarter_dropdown', 'value')
)
def set_courses_options(selected_quarter):
    return [{'label': x, 'value': x} for x in get_classes_based_off_quarter(selected_quarter)]
@app.callback(
    Output('class_dropdown', 'value'),
    Input('class_dropdown', 'options')
)
def set_courses_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('professor_checklist', 'options'),
    Input('quarter_dropdown', 'value'),
    Input('class_dropdown', 'value')
)
def set_professor_options(selected_quarter, selected_class):
    return [{'label': x, 'value': x} for x in get_professor_based_off_class_and_quarter(selected_class, selected_quarter)]
@app.callback(
    Output('professor_checklist', 'value'),
    Input('professor_checklist', 'options')
)
def set_professor_value(available_options):
    return [available_options[0]['value']]

@app.callback(
    Output("bar-chart", "figure"),
    [Input("percent_dropdown", "value"), Input("quarter_dropdown", "value"), Input("class_dropdown", "value"), Input('professor_checklist', 'value')]
)


def update_bar_chart(percent, quarter, course, professors):
    # mask = df["day"] == day
    # fig = px.bar(df[mask], x="sex", y="total_bill", 
    #              color="smoker", barmode="group")
    # return fig
    # return f"From form 1: {day1}, and from form 2: {day2}"
    # app.logger.info(plot(course='MATH 8', quarter='Fall 2020', percentage=False, professors=[]))
    app.logger.info(percent)
    show_percent = True if percent == 'True' else False
    return plot(course=course, quarter=quarter, percentage=show_percent, professors=professors)

app.run_server(debug=True)