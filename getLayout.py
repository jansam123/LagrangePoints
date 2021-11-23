from dash import dcc
from dash import html
import dash_daq as daq


def getLayout(distance_table):

    return html.Div([
        html.Hr(),
        html.H5("Smaller mass [kg]"),
        dcc.Input(
            id="m1_input",
            type="number",
            placeholder="Input mass m1",
        ),
        html.Hr(),
        html.H5("Bigger mass [kg]"),
        dcc.Input(
            id="m2_input",
            type="number",
            placeholder="Input mass m2",
        ),
        html.Hr(),
        html.H5("Distance between masses [m]"),
        dcc.Input(
            id="a_input",
            type="number",
            placeholder="Input distance a",
        ),
        dcc.Dropdown(
            id='a_dropdown',
            options=[{'label': option, 'value': option}
                     for option in distance_table],
            value='Manual Entry'
        ),
        html.Hr(),
        html.H5("G [m3 kg-1 s-2]"),
        dcc.Input(
            id="G_input",
            type="number",
            placeholder="Input gravitational constat G",
        ),
        html.Button('Real value of G', id='reset-G', n_clicks=0),
        html.Hr(),
        html.P("z-axis range:"),
        dcc.RangeSlider(
            id='zrange_slider'),
        html.Button('Reset z-axis', id='resetZaxis_button', n_clicks=0),
        html.Hr(),
        html.Hr(),
        daq.ToggleSwitch(
            id='points_toggle',
            label='Show Lagrage points',
            labelPosition='bottom',
            value=True
        ),
    ], className="three columns")




