from dash import Dash, dcc, html, Input, Output
import os


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H2("'den büyük"),
    dcc.Dropdown([3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7],
        id='dropdown'
    ),
    html.Div(id='display-value')
])

@app.callback(Output('display-value', 'children'),
                [Input('dropdown', 'value')])
def display_value(value):
    return f"{value} 'den büyük"

if __name__ == '__main__':
    app.run_server(debug=True)