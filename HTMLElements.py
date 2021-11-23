from dash import html
import dash
from dash import dcc
from dataclasses import dataclass, field

distance_table = {'Earth_Sun': 147.99e9, 'Jupiter_Sun': 748.9e9, 'Saturn_Sun': 1483e10, 'Moon_Earth': 384e6,
                  'Manual_Entry': 1.2}
mass_table = {'Earth': 5.972e24, 'Saturn': 5.683e26,
              'Jupiter': 1.898e27, 'Sun': 1.989e30, 'Moon': 7.34767309e22, 'Manual': 1, 'Entry': 2}


@dataclass
class NumberInput(dcc.Input):
    name: str
    value: float
    type: str = 'number'

    def __post_init__(self):
        self.id = f'{self.name}_input'
        self.placeholder = f'Input variable {self.name}'


@dataclass
class DropdownOption:
    label: str

    def __post_init__(self):
        self.a_value = distance_table[self.label]
        self.m1_value = mass_table[self.label.split('_')[0]]
        self.m2_value = mass_table[self.label.split('_')[1]]


def dropdownOptions():
    return [{'label': option, 'value': DropdownOption(option)}
            for option in distance_table]


class MassCombinationDropdown(dcc.Dropdown):

    def __init__(self):
        self.id = 'a_dropdown'
        self.options  = field(default_factory=dropdownOptions)
        #self.value = DropdownOption('Manual_Entry')


def checklistOptions():
    return {'label': 'Show Lagrange Points', 'value': 'LP'}


@dataclass
class LpChecklist(dcc.Checklist):

    id: str = 'checklist'
    options: dict = field(default=checklistOptions)
    value: str = 'LP'


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([
        html.Hr(),
        html.H5("Smaller mass [kg]"),
        MassCombinationDropdown(),
    ], className="three columns"),
    html.Footer([
        html.P("© Samuel Jankovych"),
    ])
])

if __name__ == '__main__':
    app.run_server()
