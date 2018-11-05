from dash.dependencies import Input, Output

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.figure_factory as ff

df = pd.read_csv("a_ereignis_01_cols_MASCH_NR-BEGIN_ZEIT-BEGIN_DAT-ENDE_ZEIT-STOERTXT_NR.csv")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def precede_zero_if_one_digit(number):
    return str(number) if len(str(number)) > 1 else "0{}".format(str(number))


def seconds_to_time(s):
    hours, minutes, seconds = "00", "00", "00"
    if s > 3600:
        hours_and_rest = divmod(s, 3600)
        hours = precede_zero_if_one_digit(hours_and_rest[0])
        s = hours_and_rest[1]
    if s > 60:
        minutes_and_rest = divmod(s, 60)
        minutes = precede_zero_if_one_digit(minutes_and_rest[0])
        s = minutes_and_rest[1]
    if 0 < s < 60:
        seconds = precede_zero_if_one_digit(s)
    return "{}:{}:{}".format(hours, minutes, seconds)


def month_day_year_to_year_month_day(date_string):
    date_array = date_string.split('/')
    return '{}-{}-{}'.format(date_array[2], date_array[0], date_array[1])


df.BEGIN_ZEIT = df['BEGIN_ZEIT'].apply(seconds_to_time)
df.ENDE_ZEIT = df['ENDE_ZEIT'].apply(seconds_to_time)
df.BEGIN_DAT = df['BEGIN_DAT'].apply(month_day_year_to_year_month_day)

unique_machines = df["MASCH_NR"].unique()

app.layout = html.Div([
    dcc.Location(id='location', refresh=False),
    dcc.Graph(
        id='invisible_graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'x'},
            ],
            'layout': {
                'title': 'invisible'
            }
        },
        style={
            'display': 'none'
        }
    ),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='dropdown_machines',
                options=[{'label': i, 'value': i} for i in unique_machines],
                value='',
                multi=True,
                placeholder='Select a machine'
            )],
        ),
    ]),
    html.Div(
        id='graph_container'
    ),
])


@app.callback(
    Output('graph_container', 'children'),
    [Input('dropdown_machines', 'value')]
)
def create_gantt_graphs(dropdown_machines):
    gantt_graphs = []
    for machine in dropdown_machines:
        machine_df = []
        for index, row in df.iterrows():
            if row['MASCH_NR'] == machine:
                entry = {
                    'Task': row['STOERTXT_NR'],
                    'Start': row['BEGIN_DAT'] + ' ' + row['BEGIN_ZEIT'],
                    'Finish': row['BEGIN_DAT'] + ' ' + row['ENDE_ZEIT']
                }
                machine_df.append(entry)

                graph = ff.create_gantt(
                    machine_df,
                    index_col='Task',
                    title=machine,
                    colors=['#333F44', '#93e4c1'],
                    show_colorbar=True,
                    showgrid_x=True,
                    showgrid_y=True
                )
                gantt_graphs.append(dcc.Graph(id='graph_' + machine, figure=graph))
    return html.Div(
        gantt_graphs
    )


if __name__ == '__main__':
    app.run_server()
