from click import style
# from matplotlib.pyplot import table
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

df = pd.read_csv('Dados_SUS.csv', on_bad_lines='skip', delimiter=';')
df = df.replace('-', 0)
df['Valor'] = df['Valor'].astype(int)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app = Dash(__name__)

opcoes = list(df['Grupo CID-10'].unique())
opcoes.append("Todas as Doenças")

app.layout = html.Div([
    html.H1(children='Análise de mortes no Ceará.', style={'color' : 'white', 'textAlign' : 'center'}),
    html.P(children='Essa é uma pequena demonstração em dashboard das morte no Ceará nos anos de 2016 a 2020.', style={'color' : 'white', 'textAlign' : 'center'}),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        df['Ano'].min(),
        df['Ano'].max(),
        step=None,
        value=df['Ano'].min(),
        marks={str(Ano): str(Ano) for Ano in df['Ano'].unique()},
        id='year-slider'
    ),
    html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Total de Mortes',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Esse é o total de mortes por faixa etária em todos os anos.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

     html.Div(children='Escolha a causa da morte desejada para visualização', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Dropdown(opcoes, value='Acidentes', id='lista_doencas'),

    dcc.Graph(
        id='fig_barras'
    )
]),
    html.P(children=' Fonte: MS/SVS/CGIAE - Sistema de Informações sobre Mortalidade - SIM Consulte o site da Secretaria Estadual de Saúde para mais informações.', style={'color': 'white', 'backgroundColor': 'grey'}),
], style={'backgroundColor' : 'black'})

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.Ano == selected_year]

    fig = px.scatter(filtered_df, x="Valor", y="Valor",
                     size="Valor", color="Faixa Etária", hover_name="Grupo CID-10",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig

@app.callback(
    Output('fig_barras', 'figure'),
    Input('lista_doencas', 'value')
    )   
def update_figure(value):
    if value == "Todas as Doenças":
        fig_barras = px.bar(df, x="Grupo CID-10", y="Valor", color="Faixa Etária", barmode="group")
    else:
        tabela_filtrada = df.loc[df["Grupo CID-10"] == value, :]
        fig_barras = px.bar(tabela_filtrada, x="Grupo CID-10", y="Valor", color="Faixa Etária", barmode="group")
    return fig_barras

if __name__ == '__main__':
    app.run_server(debug=True)