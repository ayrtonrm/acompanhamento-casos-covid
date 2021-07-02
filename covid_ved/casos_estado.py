import json
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from data import df

with open('./datasets/brazil_geo.json') as response:
    ufs = json.load(response)


fig = px.choropleth(
                data_frame=df[(df['is_last']) & (df['place_type'] == 'state')],
                center={'lat': -21.478316, 'lon': -49.229384},
                geojson=ufs,
                locations='state',
                color='last_available_confirmed_per_100k_inhabitants',
                color_continuous_scale="Viridis",
                range_color=[4000, 17000]
            )
fig.update_geos(fitbounds="locations", visible=False)

casos_por_estado = html.Div(
    [
        'Gráfico por estados',
        dcc.Graph(
            id='casos_estado',
            figure=fig
        )
    ],
    id='casos_por_estado'
)
