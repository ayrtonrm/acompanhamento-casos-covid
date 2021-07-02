import os

from dash.dependencies import Input, Output

from app import app
from evolucao_sp import evolucao_cidade
from casos_estado import casos_por_estado


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def criar_tabela(_):
    return [
        evolucao_cidade,
        casos_por_estado
    ]

server = app.server

if __name__ == '__main__':
    host = os.environ.get('HOST')
    port = os.environ.get('PORT')
    if host is None:
        host = '0.0.0.0'
    if port is None:
        port = 8052
    app.run_server(debug=True, host=host, port=port)
