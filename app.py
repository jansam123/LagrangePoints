import dash
from dash import dcc
from dash import html
import dash_daq as daq
from dash.dependencies import Input, Output
from LagrangePoints import LagPlot, variable_setup, calculate_LagPoints_coordinates
from getLayout import getMainLayout, getButtonLayout

app = dash.Dash(__name__)
server = app.server
app.title = 'Lagrange Points'

m1 = 1
m2 = 3
a = 1.2
G = 1

distance_table = {'Earth Sun': 147.99e9, 'Jupiter Sun': 748.9e9, 'Saturn Sun': 1483e10, 'Moon Earth': 384e6,
                  'Manual Entry': 1.2}
mass_table = {'Earth': 5.972e24, 'Saturn': 5.683e26,
              'Jupiter': 1.898e27, 'Sun': 1.989e30, 'Moon': 7.34767309e22, 'Manual': 1, 'Entry': 3}


mainPlot = LagPlot()


@app.callback([
    Output("zrange_slider", "min"),
    Output("zrange_slider", "max"),
    Output("zrange_slider", "step"),
],
    [
        Input("m1_input", "value"),
        Input("m2_input", "value"),
        Input("a_input", "value"),
        Input("G_input", "value"),
])
def add_min_max_step(m1, m2, a, G):

    scale_factor = variable_setup(m1, m2, a, G)[-1]
    min = -4*scale_factor
    max = 1*scale_factor
    step = 0.1*scale_factor
    return min, max, step


@app.callback(
    Output("zrange_slider", "value"),
    [
        Input("m1_input", "value"),
        Input("m2_input", "value"),
        Input("a_input", "value"),
        Input("G_input", "value"),
        Input('resetZaxis_button', 'n_clicks'),
    ])
def add_value_slider(m1, m2, a, G, n_clicks):
    scale_factor = variable_setup(m1, m2, a, G)[-1]
    value1 = -3*scale_factor
    value2 = 0*scale_factor

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
    return mass_table[name.split(' ')[0]], mass_table[name.split(' ')[1]], distance_table[name]


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


@app.callback(
    Output("scatter-plot", "figure"),
    [
        Input("zrange_slider", "value"),
        Input("m1_input", "value"),
        Input("m2_input", "value"),
        Input("a_input", "value"),
        Input("G_input", "value"),
        Input("points_toggle", "on"),
        Input("dim_toggle", "value"),
    ])
def plotly_figure(zrange, m1, m2, a, G, points, dim):
    zmin, zmax = zrange

    mainPlot.fig.data = []
    mainPlot.update_physical_variables(m1, m2, a, G)
    mainPlot.update_LagPoints()
    if dim:
        mainPlot.update_coordinates(2.5, 3)
        mainPlot.update_3Dplot(zmin, mainPlot.lagPoints[2][0])
        mainPlot.update_VeffAxis(zmin, zmax)
        if points:
            mainPlot.add_3DLagPoints()
    else:
        mainPlot.update_coordinates(2.3, 2)
        mainPlot.update_2Dplot(zmin, mainPlot.lagPoints[2][0])
        if points:
            mainPlot.add_2DLagPoints()

    return mainPlot.fig


graph = dcc.Graph(id="scatter-plot", style={'height': '95vh'})

footer = html.Footer([
    html.P("© Samuel Jankovych"),
])

app.layout = html.Div([
    html.Div([*getButtonLayout(), graph], className="nine columns"),
    html.Div(getMainLayout(distance_table), className="three columns"),
    footer
])

if __name__ == '__main__':
    app.run_server(debug=True)
