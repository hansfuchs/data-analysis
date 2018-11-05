import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("a_ereignis_01_cols_MASCH_NR-BEGIN_ZEIT-BEGIN_DAT-ENDE_ZEIT-STOERTXT_NR.csv")

# df = [dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28'),
#      dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15'),
#      dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30')]

# Start=BEGIN_DAT+BEGIN_ZEIT, Finish=BEGIN_DAT+END_ZEIT


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
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='dropdown_machines',
                options=[{'label': i, 'value': i} for i in unique_machines],
                value=unique_machines[0],
                multi=True
            )],),
    ]),
    #dcc.Graph(id='gantt')
])



'''
fig = ff.create_gantt(
    df,
    index_col='Task',
    title='Daily Schedule',
    colors=colors,
    show_colorbar=True,
    showgrid_x=True,
    showgrid_y=True)

app.layout = html.Div([
    
])
'''

@app.callback(
    Output('gantt', 'figure'),
    [Input('dropdown_machines', 'value')]
)
def update_gantt(dropdown_machines):
    machine_df, colors = [], []
    for row in df:
        if row.MASCH_NR == dropdown_machines:
            entry = {
                'Task': row.STOERTXT_NR,
                'Start': row.BEGIN_DAT + row.BEGIN_ZEIT,
                'Finished': row.BEGIN_DAT + row.ENDE_ZEIT
            }
            machine_df.append(entry)

        if empty(colors):

    return ff.create_gantt(
        machine_df,
        index_col='Task',
        title='Daily Schedule',
        colors=colors,
        show_colorbar=True,
        showgrid_x=True,
        showgrid_y=True
    )


if __name__ == '__main__':
    # app.run_server()
    print(df['BEGIN_DAT'])
