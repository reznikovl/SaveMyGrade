import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from savemygrade import *


app = dash.Dash(title='Save My Grade!', external_stylesheets=[dbc.themes.UNITED])
font = 'Verdana'

default_store = {'stored_quarters': [], 'stored_department': 0, 'stored_number': 0, 'stored_professors': [], 'stored_percent': 0}
default_store_index = {'stored_department': 0, 'stored_professor': 0 }

populate_quarter_sheets()

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Disbtributions", href="/")),
            dbc.NavItem(dbc.NavLink("Professors", href="/professors")),
            dbc.NavItem(dbc.NavLink("About", href="/about")),
        ],
        brand="Save My Grade!",
        brand_href="/",
        color="primary",
        dark=True,
        links_left=True,
        fluid=True,
        style={'padding-left': '170px'}
    ),
    html.Div(id='page-content', style={'padding-left': '180px', 'padding-right': '180px', 'padding-top': '30px', 'padding-bottom': '0px'})
], style={'font-family': font})

main_page_layout = html.Div([
    dcc.Store(id='local', storage_type='session'),
    html.H2('Course Distributions'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.H6('Quarter'),
                html.Div([
                    html.Button(
                        'All',
                        id='select-all-quarter',
                        className='btn btn-light btn-sm',
                        style={'padding': '0.1rem 0.5rem'}
                    )
                ], style={'padding-left': '8px', 'margin-top': '-5px'}),
                html.Div([
                    html.Button(
                        'None',
                        id='select-none-quarter',
                        className='btn btn-light btn-sm',
                        style={'padding': '0.1rem 0.5rem'}
                    )
                ], style={'padding-left': '8px', 'margin-top': '-5px'}),
                html.Div([
                    html.Button(
                        'Summer',
                        id='select-summer',
                        className='btn btn-light btn-sm',
                        style={'padding': '0.1rem 0.5rem'}
                    )
                ], style={'padding-left': '8px', 'margin-top': '-5px'}),
                html.Div([
                    html.Button(
                        'Fall',
                        id='select-fall',
                        className='btn btn-light btn-sm',
                        style={'padding': '0.1rem 0.5rem'}
                    )
                ], style={'padding-left': '8px', 'margin-top': '-5px'}),
                html.Div([
                    html.Button(
                        'Winter',
                        id='select-winter',
                        className='btn btn-light btn-sm',
                        style={'padding': '0.1rem 0.5rem'}
                    )
                ], style={'padding-left': '8px', 'margin-top': '-5px'}),
                html.Div([
                    html.Button(
                        'Spring',
                        id='select-spring',
                        className='btn btn-light btn-sm',
                        style={'padding': '0.1rem 0.5rem'}
                    )
                ], style={'padding-left': '8px', 'margin-top': '-5px'})
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id="quarter_dropdown",
                        options=[{"label": x, "value": x} for x in reversed(get_quarters())],
                        value=['Winter 2020'],
                        multi=True
                    )
                ], style={'padding': '0px'})
            ])
        ], style={'padding-left': '30px', 'padding-right': '30px'}),
        dbc.Col([
            html.H6('Dept.'),
            dcc.Dropdown(
                id="department_dropdown",
                clearable=False
            )
        ], width=1, style={'padding-right': '0px', 'margin-right': '0px'}),
        dbc.Col([
            html.H6('#'),
            dcc.Dropdown(
                id="number_dropdown",
                clearable=False
            ),
        ], width=1, style={'padding-left': '0px', 'margin-left': '0px'}),
        dbc.Col([
            dbc.Row([
                html.H6('Professors'),
                html.Div([
                    html.Button(
                        'All',
                        id='select-all-prof',
                        className='btn btn-light btn-sm',
                        style={'padding': '0.1rem 0.5rem'}
                    )
                ], style={'padding-left': '8px', 'margin-top': '-5px'}),
                html.Div([
                    html.Button(
                        'None',
                        id='select-none-prof',
                        className='btn btn-light btn-sm',
                        style={'padding': '0.1rem 0.5rem'}
                    )
                ], style={'padding-left': '8px', 'margin-top': '-5px'})
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id="professor_dropdown",
                        multi=True
                    )
                ], style={'padding': '0px'})
            ])
        ], style={'padding-left': '30px', 'padding-right': '30px'}),
        dbc.Col([
            html.H6('Y-Axis Data'),
            dcc.Dropdown(
                id="percent_dropdown",
                options=[{'label': 'Percent of Students', 'value': 'True'}, {'label': 'Number of Students', 'value': 'False'}],
                clearable=False
            )
        ], width=2),
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id="bar-chart"), width=7
        ),
        dbc.Col(
            dash_table.DataTable(
                id='statistics_table',
                columns=[{'name': 'Professor', 'id': 'Professor'}, {'name': 'Median', 'id': 'Median'}, {'name': 'Average', 'id': 'Average'}, {'name': 'Standard Deviation', 'id': 'Standard Deviation'}],
                sort_action="native",
                sort_mode="multi",
                style_table={'overflowX': 'auto'},
                style_cell={
                    'minWidth': '50px', 'width': '50px', 'maxWidth': '300px', 'textAlign': 'left', 'padding': '8px 8px',
                    'font-family': font
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(240, 240, 240)'
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(225, 225, 225)'
                }
            ), width=5
        )
    ])
])

# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

@app.callback(
    Output('quarter_dropdown', 'value'),
    Output('select-all-quarter', 'n_clicks'),
    Output('select-none-quarter', 'n_clicks'),
    Output('select-summer', 'n_clicks'),
    Output('select-fall', 'n_clicks'),
    Output('select-winter', 'n_clicks'),
    Output('select-spring', 'n_clicks'),
    Input('quarter_dropdown', 'options'),
    Input('select-all-quarter', 'n_clicks'),
    Input('select-none-quarter', 'n_clicks'),
    Input('select-summer', 'n_clicks'),
    Input('select-fall', 'n_clicks'),
    Input('select-winter', 'n_clicks'),
    Input('select-spring', 'n_clicks'),
    State('local', 'data'),
    
)
def set_quarters_value(available_options, all_clicks, none_clicks, summer_clicks, fall_clicks, winter_clicks, spring_clicks, storage):
    if all_clicks:
        return [i['value'] for i in available_options], 0, 0, 0, 0, 0, 0
    elif none_clicks:
        return [], 0, 0, 0, 0, 0, 0
    elif summer_clicks:
        return [i['value'] for i in available_options if i['value'].startswith('Summer')], 0, 0, 0, 0, 0, 0
    elif fall_clicks:
        return [i['value'] for i in available_options if i['value'].startswith('Fall')], 0, 0, 0, 0, 0, 0
    elif winter_clicks:
        return [i['value'] for i in available_options if i['value'].startswith('Winter')], 0, 0, 0, 0, 0, 0
    elif spring_clicks:
        return [i['value'] for i in available_options if i['value'].startswith('Spring')], 0, 0, 0, 0, 0, 0
    elif storage and 'stored_quarters' in storage and storage['stored_quarters']:
        return storage['stored_quarters'], 0, 0, 0, 0, 0, 0
    return [available_options[0]['value']], 0, 0, 0, 0, 0, 0

# Department
@app.callback(
    Output('department_dropdown', 'options'),
    Input('quarter_dropdown', 'value')
)
def set_departments_options(selected_quarters):
    if selected_quarters == []:
        raise PreventUpdate
    return [{'label': x, 'value': x} for x in get_departments_based_off_quarter(selected_quarters)]

@app.callback(
    Output('department_dropdown', 'value'),
    Input('department_dropdown', 'options'),
    State('local', 'data')
)
def set_departments_value(available_options, storage):
    if storage and 'stored_department' in storage and storage['stored_department'] in [h['value'] for h in available_options]:
        return storage['stored_department']
    return available_options[0]['value']

# Number
@app.callback(
    Output('number_dropdown', 'options'),
    Input('quarter_dropdown', 'value'),
    Input('department_dropdown', 'value')
)
def set_numbers_options(selected_quarters, selected_department):
    if selected_quarters == []:
        raise PreventUpdate
    numbers = get_numbers_based_off_quarters_and_department(selected_quarters, selected_department)
    return [{'label': x, 'value': x} for x in numbers]

@app.callback(
    Output('number_dropdown', 'value'),
    Input('number_dropdown', 'options'),
    State('local', 'data')
)
def set_numbers_value(available_options, storage):
    if available_options == []:
        raise PreventUpdate
    if storage and 'stored_number' in storage and storage['stored_number'] in [h['value'] for h in available_options]:
        return storage['stored_number']
    return available_options[0]['value']

# Professor
@app.callback(
    Output('professor_dropdown', 'options'),
    Input('quarter_dropdown', 'value'),
    Input('department_dropdown', 'value'),
    Input('number_dropdown', 'value')
)
def set_professor_options(selected_quarters, selected_department, selected_number):
    if selected_quarters == []:
        raise PreventUpdate
    professors = get_professor_based_off_class_and_quarter(selected_department + " " + selected_number, selected_quarters)
    return [{'label': x, 'value': x} for x in professors]

@app.callback(
    Output('professor_dropdown', 'value'),
    Output('select-all-prof', 'n_clicks'),
    Output('select-none-prof', 'n_clicks'),
    Input('professor_dropdown', 'options'),
    Input('select-all-prof', 'n_clicks'),
    Input('select-none-prof', 'n_clicks'),
    State('local', 'data'),
)
def set_professor_value(available_options, all_clicks, none_clicks, storage):
    if all_clicks:
        return [i['value'] for i in available_options], 0, 0
    elif none_clicks:
        return [], 0, 0
    else:
        if available_options == []:
            return [], 0, 0
        professors = []
        for o in available_options:
            if storage and 'stored_professors' in storage and o['value'] in storage['stored_professors']:
                professors.append(o['value'])
        if professors == []:
            return [available_options[0]['value']], 0, 0
        return professors, 0, 0

# Percent
@app.callback(
    Output('percent_dropdown', 'value'),
    Input('percent_dropdown', 'options'),
    State('local', 'data')
)
def set_percent_value(available_options, storage):
    if storage and 'stored_percent' in storage and storage['stored_percent']:
        return storage['stored_percent']
    return available_options[0]['value']

# Plot
@app.callback(
    Output("bar-chart", "figure"),
    Output("bar-chart", "config"),
    Output('statistics_table', 'data'),
    Output('local', 'data'),
    Input("percent_dropdown", "value"),
    Input("quarter_dropdown", "value"),
    Input("department_dropdown", "value"),
    Input("number_dropdown", "value"),
    Input('professor_dropdown', 'value'),
    State('local', 'data')
)
def update_bar_chart(percent, quarters, department, number, professors, storage):
    if quarters == []:
        raise PreventUpdate
    if not storage or storage.keys is not default_store.keys:
        storage = default_store
    storage['stored_quarters'] = quarters
    storage['stored_department'] = department
    storage['stored_number'] = number
    storage['stored_percent'] = percent
    storage['stored_professors'] = professors
    fig, statistics = plot(course=department+" "+number, quarters=quarters, percentage=percent=='True', professors=professors)
    config = {'displayModeBar': False}
    return fig, config, statistics, storage

# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

professor_page_layout = html.Div([
    dcc.Store(id='local_index', storage_type='session'),
    html.H2('Professor History'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H6('Department'),
            dcc.Dropdown(
                id="department_dropdown_index",
                options=[{"label": x, "value": x} for x in get_departments_based_off_quarter(get_quarters())]
            )
        ], width=2),
        dbc.Col([
            html.H6('Professor'),
            dcc.Dropdown(
                id="professor_dropdown_index"
            )
        ], width=2),
        dbc.Col([
            dcc.Checklist(
                options=[{'label': ' Show Pass/Fail Courses', 'value': 'show_na'}],
                id="show_na_check"
            )
        ], width=2)
    ]),
    html.Br(),
    dash_table.DataTable(
        id='statistics_table_index',
        columns=[{'name': 'Quarter', 'id': 'Quarter'}, {'name': 'Course', 'id': 'Course'}, {'name': 'Median', 'id': 'Median'}, {'name': 'Average', 'id': 'Average'}, {'name': 'Standard Deviation', 'id': 'Standard Deviation'}],
        sort_action="native",
        sort_mode="multi",
        style_table={'overflowX': 'auto', 'maxWidth': '600px'},
        style_cell={
            'minWidth': '50px', 'maxWidth': '300px', 'textAlign': 'left', 'padding': '8px 8px',
            'font-family': font
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(240, 240, 240)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(225, 225, 225)'
        }
    ),
    html.Br(),
    dash_table.DataTable(
        id='statistics_table_index_cumulative',
        columns=[{'name': 'Overall Median', 'id': 'Overall Median'}, {'name': 'Overall Average', 'id': 'Overall Average'}, {'name': 'Overall Standard Deviation', 'id': 'Overall Standard Deviation'}],
        sort_action="native",
        sort_mode="multi",
        style_table={'overflowX': 'auto', 'maxWidth': '600px'},
        style_cell={
            'minWidth': '150px', 'maxWidth': '300px', 'textAlign': 'left', 'padding': '8px 8px',
            'font_family': font
        },
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

about_page_layout = html.Div([
    dcc.Store(id='local_index', storage_type='session'),
    html.H2('About'),
    html.Br(),
    html.H6('Save My Grade is a web application to view grade distributions and professor statistics for UCSB. Data is currently available from Fall 2015 to Winter 2021'),
    html.Br(),
    html.H6('Developed by Brandon Nadell and Leron Reznikov')
])

# Quarter
@app.callback(
    Output('department_dropdown_index', 'value'),
    Input('department_dropdown_index', 'options'),
    State('local_index', 'data')
)
def set_department_index_value(available_options, storage):
    if storage and 'stored_department' in storage:
        return storage['stored_department']
    return available_options[0]['value']

# Professor
@app.callback(
    Output('professor_dropdown_index', 'options'),
    Input('department_dropdown_index', 'value')
)
def set_professor_index_options(selected_department):
    return [{'label': x, 'value': x} for x in get_professor_based_off_department(selected_department)]

@app.callback(
    Output('professor_dropdown_index', 'value'),
    Input('professor_dropdown_index', 'options'),
    State('local_index', 'data')
)
def set_professor_index_value(available_options, storage):
    if storage and 'stored_professor' in storage and storage['stored_professor'] in [h['value'] for h in available_options]:
        return storage['stored_professor']
    return available_options[0]['value']

# # Show N/A
# @app.callback(
#     Output('show_na_check', 'options'),
#     Input('show_na_check', 'value')
# )
# def set_show_na_value(show_na):
#     return True

# Table
@app.callback(
    Output('statistics_table_index', 'data'),
    Output('statistics_table_index_cumulative', 'data'),
    Output('local_index', 'data'),
    Input('department_dropdown_index', 'value'),
    Input('professor_dropdown_index', 'value'),
    Input('show_na_check', 'value'),
    State('local_index', 'data')
)

def set_table(department, professor, show_na, storage):
    if not storage or storage.keys is not default_store_index.keys:
        storage = default_store_index
    storage['stored_department'] = department
    storage['stored_professor'] = professor
    stats = get_statistics_of_professor(professor, show_na)
    return stats[0], stats[1], storage


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return main_page_layout
    elif pathname == '/professors':
        return professor_page_layout
    elif pathname == '/about':
        return about_page_layout
    return html.Div('404: Page not found')

app.run_server(
debug=True,
dev_tools_ui=False
, host='0.0.0.0')
# app.config.suppress_callback_exceptions = False
