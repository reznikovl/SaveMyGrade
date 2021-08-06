import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from savemygrade import *


app = dash.Dash(__name__)

dropdown_width='60%'

dataframe = None
default_percent = 'True'
default_course = None
populate_quarter_sheets()

app.layout = html.Div([
    html.Center(html.H1('Let\'s Save Your Grade!')),
    'Quarter',
    dcc.Checklist(
        id="quarter_checklist",
        options=[{"label": x, "value": x} for x in reversed(get_quarters())],
        value=['Winter 2020'],
        style={'width': dropdown_width},
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
        value=default_percent,
        style={'width': dropdown_width},
        clearable=False,
    ),

    html.Br(),
    'Professors:',
    dcc.Checklist(
        id="professor_checklist",
        labelStyle={'display': 'block'}
        # labelStyle={'display': 'flex', 'flexFlow': 'row wrap'}
    ),
    dcc.Graph(id="bar-chart"),
    dash_table.DataTable(
        id='statistics_table',
        columns=[{'name': 'Professor', 'id': 'Professor'}, {'name': 'Median', 'id': 'Median'}, {'name': 'Average', 'id': 'Average'}, {'name': 'Standard Deviation', 'id': 'Standard Deviation'}],
        style_table={'overflowX': 'auto', 'width': '750px'},
        style_cell={
            'minWidth': '150px', 'width': '150px', 'maxWidth': '300px', 'textAlign': 'left',
            'font_family': 'Open Sans'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'Professor'},
            'width': '200%'}
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(240, 240, 240)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(225, 225, 225)'
        }
    )
])

@app.callback(
    Output('class_dropdown', 'options'),
    Input('quarter_checklist', 'value')
)

def set_courses_options(selected_quarters):
    return [{'label': x, 'value': x} for x in get_classes_based_off_quarter(selected_quarters)]

@app.callback(
    Output('class_dropdown', 'value'),
    Input('class_dropdown', 'options')
)

def set_courses_value(available_options):
    if default_course in [h['value'] for h in available_options]:
        return default_course
    return available_options[0]['value']

@app.callback(
    Output('professor_checklist', 'options'),
    Input('quarter_checklist', 'value'),
    Input('class_dropdown', 'value')
)

def set_professor_options(selected_quarters, selected_class):
    global dataframe
    professors, dataframe = get_professor_based_off_class_and_quarter(selected_class, selected_quarters)
    return [{'label': x, 'value': x} for x in professors]

@app.callback(
    Output('professor_checklist', 'value'),
    Input('professor_checklist', 'options')
)

def set_professor_value(available_options):
    return [available_options[0]['value']]

@app.callback(
    Output("bar-chart", "figure"),
    [Input("percent_dropdown", "value"), Input("quarter_checklist", "value"), Input("class_dropdown", "value"), Input('professor_checklist', 'value')]
)

def update_bar_chart(percent, quarters, course, professors):
    global default_percent, default_course
    default_percent = percent
    default_course = course
    show_percent = True if percent == 'True' else False
    return plot(course=course, quarters=quarters, percentage=show_percent, professors=professors, dataframe=dataframe)

@app.callback(
    Output('statistics_table', 'data'),
    Input('bar-chart', 'figure')
)

def update_table(figure):
    return getStatistics()

app.run_server(debug=True, host='0.0.0.0')