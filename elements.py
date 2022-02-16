import dash_html_components as html

font = 'Verdana'

default_store = {'stored_quarters': [], 'stored_department': 0, 'stored_number': 0, 'stored_professors': [], 'stored_percent': 'percent'}
default_store_index = {'stored_department': 0, 'stored_professor': 0 }

no_margin = {'margin-left': '-15px'}

table_style_data_conditional=[
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(240, 240, 240)'
    }
]
table_style_header={
    'backgroundColor': 'rgb(225, 225, 225)'
}
checklistStyle={'display': 'block', 'margin-bottom': '0.0rem'}

professor_table_options = [
    {'name': 'Professor', 'id': 'professor'}, 
    {'name': 'Quarter', 'id': 'quarter'}, 
    {'name': 'Course', 'id': 'course'}, 
    {'name': 'Median', 'id': 'median'}, 
    {'name': 'Average', 'id': 'average'}, 
    {'name': 'Deviation', 'id': 'deviation'}, 
    {'name': 'Count', 'id': 'count'}, 
    {'name': 'Rating', 'id': 'rating', 'type': 'text', 'presentation': 'markdown'},
]

table_cumulative_options = [
    {'name': 'Overall Median', 'id': 'median'},
    {'name': 'Overall Average', 'id': 'average'},
    {'name': 'Overall Deviation', 'id': 'deviation'},
]



def select_button(name, Id):
    return html.Div([
        html.Button(
            name,
            id=Id,
            className='btn btn-light btn-sm select-button'
        )
    ], className='select-button-div')