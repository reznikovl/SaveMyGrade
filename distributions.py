import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from savemygrade import *
from elements import *
from server import app

main_page_layout = html.Div([
    dcc.Store(id='local', storage_type='session'),
    html.H2('Course Distributions'),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id="bar-chart"), width=7, style={'padding': '30px'}
        ),
        dbc.Col([
            dbc.Row([
                html.H6('Quarter'),
                select_button('All', 'select-all-quarter'),
                select_button('None', 'select-none-quarter'),
                select_button('Summer', 'select-summer'),
                select_button('Fall', 'select-fall'),
                select_button('Winter', 'select-winter'),
                select_button('Spring', 'select-spring')
            ]),
            dbc.Row(
                dbc.Col(
                    dcc.Dropdown(
                        id="quarter_dropdown",
                        options=[{"label": x, "value": x} for x in reversed(get_quarters())],
                        value=['Winter 2021'], multi=True, optionHeight=25
                    ), className='no-padding'
                )
            ),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H6('Dept.'),
                    dcc.Dropdown(
                        id="department_dropdown",
                        clearable=False, optionHeight=25
                    )
                ], width=3, className='no-padding'),
                dbc.Col([
                    html.H6('#'),
                    dcc.Dropdown(
                        id="number_dropdown",
                        clearable=False, optionHeight=25
                    ),
                ], width=3, className='no-padding')
            ]),
            html.Br(),
            dbc.Row([
                html.H6('Professors'),
                select_button('All', 'select-all-prof'),
                select_button('None', 'select-none-prof')
            ]),
            dbc.Row(
                dbc.Col(
                    dcc.Dropdown(
                        id="professor_dropdown",
                        multi=True, optionHeight=25
                    ), className='no-padding'
                )
            ),
            html.Br(),
            dbc.Row(
                dcc.RadioItems(
                    id="percent_dropdown",
                    options=[{'label': ' Show Percent of Student', 'value': 'percent'}, {'label': ' Show Number of Students', 'value': 'number'}],
                    value='percent', labelStyle=checklistStyle
                )
            )
        ], width=5, style={'padding': '30px'})
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='statistics_table',
                columns=[professor_table_options[0], professor_table_options[3], professor_table_options[4]],
                sort_action="native", sort_mode="multi",
                style_cell={'padding': '8px 8px', 'font-family': font}, style_data_conditional=table_style_data_conditional, style_header=table_style_header
            ),
            html.Br(),
            html.H6('* may be inaccurate due to too few ratings', style={'font-size': '.8rem', 'margin-bottom': '0rem'}),
            html.I('Rating data is taken from ratemyprofessor.com and may contain errors', style={'font-size': '.8rem'})
        ], width=7, style={'padding': '30px'}),
        dbc.Col(
            dcc.Checklist(
                id="professor_table_options",
                options=[{'label': ' Show Standard Deviation', 'value': 'deviation'}, {'label': ' Show Student Count', 'value': 'count'}, {'label': ' Show Rating', 'value': 'rating'}],
                labelStyle=checklistStyle, style={'padding-top': '30px'}
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
    fig, statistics = plot(course=department+" "+number, quarters=quarters, percentage=percent=='percent', professors=professors)
    config = {'displayModeBar': False}
    return fig, config, statistics, storage

@app.callback(
    Output('statistics_table', 'columns'),
    Input('professor_table_options', 'value')
)

def update_columns(checked_column_names):
    return [i for i in professor_table_options
        if i['id'] in ['professor', 'average', 'median']
        + (checked_column_names or [])]

