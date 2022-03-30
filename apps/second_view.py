from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from app import app
import pandas as pd
import functions as fc

dataframe = pd.DataFrame()

CANDIDAT_OPTIONS = [
    {'label':'All', 'value':'All'},
    {'label':'Emmanuel Macron', 'value':'Macron'},
    {'label':'Nathalie Arthaud', 'value':'Arthaud'},
    {'label':'Fabien Roussel', 'value':'Roussel'},
    {'label':'Jean Lassalle', 'value':'Lassalle'},
    {'label':'Marine Le Pen', 'value':'Le Pen'},
    {'label':'Éric Zemmour', 'value':'Zemmour'},
    {'label':'Jean-Luc Mélenchon', 'value':'Melenchon'},
    {'label':'Anne Hidalgo', 'value':'Hidalgo'},
    {'label':'Yannick Jadot', 'value':'Jadot'},
    {'label':'Valérie Pécresse', 'value':'Pecresse'},
    {'label':'Philippe Poutou', 'value':'Poutou'},
    {'label':'Nicolas Dupont-Aignan', 'value':'Dupont_Aignan'}
]


TOP_OPTIONS = [
    {'label':' Top 5 ', 'value':5},
    {'label':' Top 10 ', 'value':10},
    {'label':' Top 15 ', 'value':15},
    {'label':' Top 20 ', 'value':20},
    {'label':' Top 25 ', 'value':25},
    {'label':' Top 30 ', 'value':30}
]

layout = dbc.Container([
    dbc.Row([
        html.H1(id='title_page2',
                children='Élection Présidentielle 2022',
                className='text-center bg-info text-white')
    ]),
    dbc.Row([
        dcc.Location(id='url2', refresh=False)
    ]),
    dbc.Row([
        dbc.Col([
            html.P('Select Candidate:', className='text-center')
        ], width=2, className='bg-light'),
        dbc.Col([
            dcc.Dropdown(id='DD-Candidat',
                         options=CANDIDAT_OPTIONS,
                          value='All', className='bg-light')
        ], width=3, className='bg-light'),
        dbc.Col([
            html.Button(id='bp-1', children=[html.I(className="fa fa-refresh m-1")])
        ], width=1, className='bg-light'),
        dbc.Col([
            html.P('Select Candidate:', className='text-center')
        ], width=2, className='bg-light'),
        dbc.Col([
            dcc.Dropdown(id='DD-Candidat2',
                         options=CANDIDAT_OPTIONS,
                          value='All', className='bg-light')
        ], width=3, className='bg-light'),
        dbc.Col([
            html.Button(id='bp-2', children=[html.I(className="fa fa-refresh m-1")])
        ], width=1, className='bg-light')
    ]),

    dbc.Row([
        dbc.Col([
            dcc.RadioItems(id='top-1',
                           options=TOP_OPTIONS,
                           value=10,
                           inline=True,
                           className='bg-light')
        ], width=6, className='bg-light'),
        dbc.Col([
            dcc.RadioItems(id='top-2',
                           options=TOP_OPTIONS,
                           value=10,
                           inline=True,
                           className='bg-light')
        ], width=6, className='bg-light')
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='htag-plot',figure={})
        ], width=6, className='bg-light'),
        dbc.Col([
            dcc.Graph(id='tag-plot',figure={})
        ], width=6, className='bg-light')
    ])

])

@app.callback(
    Output(component_id='htag-plot', component_property='figure'),
    [Input(component_id='bp-1', component_property='n_clicks')],
    [State(component_id='DD-Candidat', component_property='value'),
     State(component_id='top-1', component_property='value')],
    prevent_initial_call=True
)
def update_htagplot(n, candidate, kpi):
    if candidate == 'All':
        df = fc.count_htags(dataframe)
    else:
        df = fc.candiate_filter(dataframe, candidate)
        df = fc.count_htags(df)

    figure={}
    figure['data'] = [go.Bar(x=df.head(kpi)['hashtag'], y=df.head(kpi)['counts'])]
    figure['layout'] = go.Layout(xaxis={'title':'Hashtags'}, yaxis={'title':'Counts'})
    return figure

@app.callback(
    Output(component_id='tag-plot', component_property='figure'),
    [Input(component_id='bp-2', component_property='n_clicks')],
    [State(component_id='DD-Candidat2', component_property='value'),
     State(component_id='top-2', component_property='value')],
    prevent_initial_call=True
)
def update_tagplot(n, candidate, kpi):
    if candidate == 'All':
        df = fc.count_tags(dataframe)
    else:
        df = fc.candiate_filter(dataframe, candidate)
        df = fc.count_tags(df)
    figure={}
    figure['data'] = [go.Bar(x=df.head(kpi)['tag'], y=df.head(kpi)['counts'])]
    figure['layout'] = go.Layout(xaxis={'title':'Accounts Taged'}, yaxis={'title':'Counts'})
    return figure

@app.callback(
    Output(component_id='title_page2', component_property='children'),
    [Input(component_id='url2', component_property='pathname')],
    prevent_initial_call=False
)
def read_data(p_name):
    global dataframe
    dataframe = pd.read_csv('datasets/tweets_prez.csv', encoding='utf-8-sig')
    dataframe = fc.data_processing(dataframe)
    return 'Élection Présidentielle 2022'
