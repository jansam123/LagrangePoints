from dash import dcc
from dash import html
import dash_daq as daq


def getMainLayout(distance_table):

    return [
        html.Tbody([
        html.Tr([
            html.Td(html.H6("2D")),
            html.Td(daq.ToggleSwitch(id='dim_toggle', value=True)),
            html.Td(html.H6("3D")),
        ])]),
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
        html.H6("Height of the potential (z-axis range)"),
        dcc.RangeSlider(
            id='zrange_slider'),
        html.Button('Reset potential (z-axis)',
                    id='resetZaxis_button', n_clicks=0),
        html.Hr(),
        html.Hr(),
        html.P("If you want to see exact coordinates of Lagrange points, hover over points with your mouse."),
        html.Tr([
        html.Td(html.P("Show Lagrage points")),
        html.Td(daq.BooleanSwitch(id='points_toggle',on=True))
        ]),
    ]


def getButtonLayout():
    info_button_style = {
        'background-color':  'green',
        'color': 'white',
        'font-size':15,

    }  
    return [
        html.Button(dcc.Link('INFO', href='#info', target="_top", style={"color": "white", "text-decoration": "none"
                                                                         }),
                    id='info_page', n_clicks=1, style=info_button_style),
    ]
