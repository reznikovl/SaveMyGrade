import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from server import app
from elements import *
from savemygrade import populate_quarter_sheets

populate_quarter_sheets()

from distributions import main_page_layout
from professors import professor_page_layout

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Distributions", href="/")),
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

about_page_layout = html.Div([
    html.H2('About'),
    html.Br(),
    html.H6('Save My Grade is a web application to view grade distributions and professor statistics for UCSB. Data is currently available from Fall 2015 to Winter 2021'),
    html.Br(),
    html.H6('Developed by Brandon Nadell and Leron Reznikov')
])

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
debug=False,
dev_tools_ui=False
, host='0.0.0.0')
# app.config.suppress_callback_exceptions = False
