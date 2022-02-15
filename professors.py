import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from savemygrade import *
from elements import *
from server import app

professor_page_layout = html.Div([
    dcc.Store(id='local_index', storage_type='session'),
    html.H2('Professor History'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H6('Department'),
            dcc.Dropdown(
                id="department_dropdown_index",
                options=[{"label": x, "value": x} for x in get_departments_based_off_quarter(get_quarters())],
                optionHeight=25
            )
        ], width=2),
        dbc.Col([
            html.H6('Professor'),
            dcc.Dropdown(
                id="professor_dropdown_index",
                optionHeight=25
            )
        ], width=2),
        dbc.Col(
            dcc.Checklist(
                id="index_table_options",
                options=[{'label': ' Show Pass/Fail Courses', 'value': 'show_na'}, {'label': ' Show Standard Deviation', 'value': 'deviation'}, {'label': ' Show Student Count', 'value': 'count'}],
                labelStyle=checklistStyle
            )
        )
    ]),
    html.Br(),
    dash_table.DataTable(
        id='statistics_table_index',
        columns=professor_table_options[1:5],
        sort_action="native", sort_mode="multi",
        style_table={'overflowX': 'auto', 'maxWidth': '700px'},
        style_cell={'minWidth': '50px', 'maxWidth': '300px', 'textAlign': 'left', 'padding': '8px 8px', 'font-family': font},
        style_data_conditional=table_style_data_conditional, style_header=table_style_header
    ),
    html.Br(),
    dash_table.DataTable(
        id='statistics_table_index_cumulative',
        columns=table_cumulative_options[:2],
        sort_action="native", sort_mode="multi", persistence=True,
        style_table={'overflowX': 'auto', 'maxWidth': '700px', 'padding-bottom': '30px'},
        style_cell={'minWidth': '150px', 'maxWidth': '300px', 'textAlign': 'left', 'padding': '8px 8px', 'font_family': font},
        style_data_conditional=table_style_data_conditional, style_header=table_style_header
    )
])

# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

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

# Table
@app.callback(
    Output('statistics_table_index', 'data'),
    Output('statistics_table_index_cumulative', 'data'),
    Output('local_index', 'data'),
    Input('department_dropdown_index', 'value'),
    Input('professor_dropdown_index', 'value'),
    Input('index_table_options', 'value'),
    State('local_index', 'data')
)

def set_table(department, professor, checklist, storage):
    if not storage or storage.keys is not default_store_index.keys:
        storage = default_store_index
    storage['stored_department'] = department
    storage['stored_professor'] = professor
    stats = get_statistics_of_professor(professor, 'show_na' in checklist if checklist else False)
    return stats[0], stats[1], storage

@app.callback(
    Output('statistics_table_index', 'columns'),
    Output('statistics_table_index_cumulative', 'columns'),
    Input('index_table_options', 'value')
)

def update_columns(checked_column_names):
    return [i for i in professor_table_options
            if i['id'] in ['quarter', 'course', 'median', 'average']
            + (checked_column_names or [])
            and i['id'] is not 'show_na'], \
        [i for i in table_cumulative_options
            if i['id'] in ['median', 'average']
            + (['deviation'] if 'deviation' in checked_column_names else [])
            and i['id'] is not 'show_na']

