import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from lagrange_points import *

df = px.data.iris()

app = dash.Dash(__name__)
server = app.server

app.title = 'Lagrange Points'
m1 = 1
m2 = 3
a = 1.2
G = 1

mass_table = {'Earth': 5.972e24, 'Saturn': 5.683e26,
              'Jupiter': 1.898e27, 'Sun': 1.989e30, 'Moon': 7.34767309e22}
distance_table = {'Earth_Sun': 147.99e9, 'Jupiter_Sun': 748.9e9, 'Saturn_Sun': 1483e10, 'Moon_Earth': 384e6
                  }

M, alpha, omega2 = variable_setup(m1, m2, a, G)
_, _, Z_lag_points = Lag_points(a, alpha, omega2, M, G)

@app.callback([
    Output("zrange-slider", "min"),
    Output("zrange-slider", "max"),
    Output("zrange-slider", "step"),
],
    [
        Input("m1_input", "value"),
        Input("m2_input", "value"),
        Input("a_input", "value"),
        Input("G_input", "value"),
])
def add_min_max_step(m1, m2, a, G):

    M, alpha, _ = variable_setup(m1, m2, a, G)
    min = -8*alpha*G*M/a
    max = 8*alpha*G*M/a
    step = 0.1*alpha*G*M/a
    return min, max, step


@app.callback(
    Output("zrange-slider", "value"),
    [
        Input("m1_input", "value"),
        Input("m2_input", "value"),
        Input("a_input", "value"),
        Input("G_input", "value"),
        Input('reset-zaxis', 'n_clicks'),
    ])
def add_value_slider(m1, m2, a, G, n_clicks):
    M, alpha, _ = variable_setup(m1, m2, a, G)
    value1 = -3*alpha*G*M/a
    value2 = 0*alpha*G*M/a

    return value1, value2


@app.callback([
    Output("m1_input", "value"),
    Output("m2_input", "value"),
    Output("a_input", "value"),
    ],
    [
        Input("a_dropdown", "value"),
    ])
def set_m(name):
    if name != '-' and name in distance_table:
        return mass_table[name.split('_')[0]], mass_table[name.split('_')[1]], distance_table[name]
    else:
        return m1, m2, a




@app.callback(
    Output("G_input", "value"),
    [
        Input("reset-G", "n_clicks"),
    ])
def set_m(n_clicks):
    if n_clicks == 0:
        return 1
    else:
        return 6.67408e-11


app.layout = html.Div([
    html.Div([
        dcc.Graph(id="scatter-plot",
                  style={'height': '100vh'}),
    ], className="nine columns"),
    html.Div([
        html.Hr(),
        html.H5("Smaller mass [kg]"),
        dcc.Input(
            id="m1_input",
            type="number",
            placeholder="Input mass m1",
            value=m1,
        ),
        html.Hr(),
        html.H5("Bigger mass [kg]"),
        dcc.Input(
            id="m2_input",
            type="number",
            placeholder="Input mass m2",
            value=m2,
        ),
        html.Hr(),
        html.H5("Distance between masses [m]"),
        dcc.Input(
            id="a_input",
            type="number",
            placeholder="Input distance a",
            value=a,
        ),
        dcc.Dropdown(
            id='a_dropdown',
            options=[
                {'label': 'Jupiter_Sun', 'value': 'Jupiter_Sun'},
                {'label': 'Saturn_Sun', 'value': 'Saturn_Sun'},
                {'label': 'Earth_Sun', 'value': 'Earth_Sun'},
                {'label': 'Moon_Earth', 'value': 'Moon_Earth'},
                {'label': 'Manual', 'value': '-'}
            ],
            value='-'
        ),
        html.Hr(),
        html.H5("G [m3 kg-1 s-2]"),
        dcc.Input(
            id="G_input",
            type="number",
            placeholder="Input gravitational constat G",
            value=G,
        ),
        html.Button('Real value of G', id='reset-G', n_clicks=0),
        html.Hr(),
        html.P("z-axis range:"),
        dcc.RangeSlider(
            id='zrange-slider'),
        html.Button('Reset', id='reset-zaxis', n_clicks=0),
        html.Hr(),
        html.Hr(),
        dcc.Checklist(
            id="checklist",
            options=[
                {'label': 'Show Lagrange Points', 'value': 'LP'}
            ],
            value=['LP']
        ),
    ], className="three columns"),
    html.Footer([
        html.P("© Samuel Jankovych"),
    ])
])


@app.callback(
    Output("scatter-plot", "figure"),
    [
        Input("zrange-slider", "value"),
        Input("m1_input", "value"),
        Input("m2_input", "value"),
        Input("a_input", "value"),
        Input("G_input", "value"),
        Input("checklist", "value"),

    ])
def plotly_figure(zrange, m1, m2, a, G, checklist):
    zmin, zmax = zrange
    show_LP = True if 'LP' in checklist else False

    M, alpha, omega2 = variable_setup(m1, m2, a, G)
    X, Y, Z = coordinates(a, alpha, omega2, M, G)
    X_lag_points, Y_lag_points, Z_lag_points = Lag_points(
        a, alpha, omega2, M, G)
    fig = run_plotly(X, Y, Z,  X_lag_points, Y_lag_points, Z_lag_points,
                     zmin=zmin,
                     zmax=zmax,
                     show_LP=show_LP
                     )

    return fig

if __name__ == '__main__':
    app.run_server()
