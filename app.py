from dash import Dash, dcc, html, Input, Output
import numpy as np
import os
#### Fetch Data

import plotly.express as px
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "http://www.koeri.boun.edu.tr/scripts/lst0.asp"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

earth_quake_data = soup.findAll('pre')

columns = ["Date", "Time", "Latitude(N)", "Longitude(E)", "Depth(km)", "Magnitude"]
magnitude_data = []

for data in earth_quake_data:
    for line in data.text.split('\n')[7:]:
        # print(line)
        splitted = re.sub(r'\s+(?!\()', ';', line.strip(' ')).split(';')
        if (len(splitted) > 6) and float(splitted[6]) > 0:
            data_required = [*splitted[0:5], float(splitted[6])]
            magnitude_data.append(data_required)

df = pd.DataFrame.from_records(magnitude_data)
df.columns = columns

####


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(id = 'parent', children = [
    html.H2('Turkiye Deprem (24 saat)'),
    html.Div(id='display-value'),

    # creating a slider within a html component 
    html.Div(id = 'slider-div', children = 
            [
                dcc.Slider(id = 'magnitude-slider',
                min = df['Magnitude'].min(),
                max = df['Magnitude'].max(),
                value = df['Magnitude'].min(),
                marks = { str(mgt) : str(mgt) for mgt in df['Magnitude'].unique() },
                step = 0.5
                )], style = {'width':'50%', 'display':'inline-block'}), 
            # inline-block : to show slider and dropdown in the same line
            # 

    # # setting the graph component 
    dcc.Graph(id = 'stamen-terrain') 
    ])


@app.callback(Output('display-value', 'children'),
                [Input(component_id='magnitude-slider', component_property= 'value')])
def display_value(value):
    return f" (>) {value}'den büyük"

## 2 input components corresponding to slider and dropdown respectively
## 1 output component corresponding to the graph 
@app.callback(Output(component_id='stamen-terrain', component_property= 'figure'),
              [Input(component_id='magnitude-slider', component_property= 'value')])
def graph_update(slider_value):
    global draw_df
    draw_df = df[df['Magnitude'] > slider_value]
    fig = px.density_mapbox(draw_df, lat='Latitude(N)', lon='Longitude(E)', z='Magnitude', radius=10,
                            center=dict(lat=39, lon=35), zoom=6, hover_data=["Date", "Time", 'Magnitude', "Depth(km)"],
                            mapbox_style="stamen-terrain", width=1600, height=800)
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
    )

    return fig

if __name__ == '__main__':
    for key in os.environ:
        print(key, '=>', os.environ[key])
    app.run_server(port=os.getenv('PORT') or 8051,host='0.0.0.0')