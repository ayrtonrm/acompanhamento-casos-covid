import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output, State
from app import app
from data import df

evolucao_cidade = html.Div(
    [
        dcc.Dropdown(id='estado', value='', options=[{'label': i, 'value': i} for i in df['state'].unique()]),
        dcc.Dropdown(id='cidade', value='', options=[{'label': '', 'value': ''}]),
        html.Div(id='chart_placeholder',),
    ],
    id='evolucao_cidade'
)


@app.callback(
    Output('cidade', 'options'),
    [Input('estado', 'value')]
)
def buscar_cidades(uf):
    if uf != '':
        cidades_repetidas = df[df['state'] == uf]['city']
        cidades = cidades_repetidas[cidades_repetidas.notnull()].sort_values().unique()
        return [{'label': i, 'value': i} for i in cidades]
    return [{'label': '', 'value': ''}]


@app.callback(
    Output('chart_placeholder', 'children'),
    [Input('cidade', 'value')],
    [State('estado', 'value')]
)
def gerar_grafico(cidade, uf):
    df_cidade = df[(df['state'] == uf) & (df['city'] == cidade) & (df['new_confirmed'] >= 0)]
    if len(df_cidade) <= 0:
        return 'Sem dados para a cidade selecionada ou a cidade não foi selecionada'
    fig = px.bar(
        df_cidade,
        x='last_available_date',
        y='new_confirmed',
        labels={'new_confirmed': 'Novos casos', 'last_available_date': 'Data'}
    )
    fig.update_xaxes(
        dtick="M1",
        tickformat="%m/%Y"
    )
    return dcc.Graph(id='grafico_evolucao_cidade', figure=fig)
