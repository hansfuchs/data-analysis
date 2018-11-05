import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("a_ereignis_01_cols_MASCH_NR-BEGIN_ZEIT-BEGIN_DAT-ENDE_ZEIT-STOERTXT_NR.csv")

available_machines = df['MASCH_NR'].unique()

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='machines',
                options=[{'label': i, 'value': i} for i in available_machines],
                value='BFO4AP01',
                multi=True
            )],),
    ]),

    dcc.Graph(id='timestamps')
])


@app.callback(
    dash.dependencies.Output('timestamps', 'figure'),
    [dash.dependencies.Input('machines', 'value'), ])
def update_graph(machines):

    return {
        'data': [
            go.Scatter(
                x=df[df['MASCH_NR'] == i]['BEGIN_ZEIT'],
                y=df[df['MASCH_NR'] == i]['ENDE_ZEIT'],
                text=df[df['MASCH_NR'] == i]['MASCH_NR'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in machines
        ],
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'BEGIN_ZEIT'},
            yaxis={'title': 'ENDE_ZEIT'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server()
