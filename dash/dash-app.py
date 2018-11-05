from datetime import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        dcc.Input(id='input_machine', type='text', value='BFO4AP01'),
        dcc.DatePickerRange(
            id='time-frame',
            min_date_allowed=dt(2010, 1, 1),
            max_date_allowed=dt(2017, 1, 1),
            initial_visible_month=dt(2016, 1, 1),
            start_date=dt(2016, 1, 1),
            end_date=dt(2017, 1, 1)
        ),
        html.Button(id='submit-button', n_clicks=0, children='Submit'),
    ]),
    dcc.Input(id='input_date_range', type='text', style='display: block', value=''),
    html.Div(id='form_input'),
])


@app.callback(
    Output('input_date_range', 'value'),
    [Input('time-frame', 'start_date'),
     Input('time-frame', 'end_date')],
)
def update_date_range(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        start_date_string = start_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        end_date_string = end_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix


@app.callback(
    Output('form_input', 'children'),
    [Input('input_machine', 'value'),
     Input('input_date_range', 'value')],
)
def update_form_input(input_machine, input_date_range):
    return input_machine + " " + input_date_range


if __name__ == '__main__':
    app.run_server(debug=True)