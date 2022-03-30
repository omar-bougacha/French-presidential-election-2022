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


KPI_OPTIONS = [
    {'label':'Number of Tweets', 'value':'number'},
    {'label':'Number of Accounts', 'value':'account'},
    {'label':'Number of Likes', 'value':'n_like'}
]

layout = dbc.Container([
    dbc.Row([
        html.H1(id='title_page', children='Élection Présidentielle 2022',
                className='text-center bg-info text-white')
    ]),
    dbc.Row([
        dcc.Location(id='url1', refresh=False)
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
        dcc.RadioItems(id='kpi-1',
                       options=KPI_OPTIONS,
                       value='number',
                       inline=True,
                       className='bg-light')
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='line-plot',figure={})
        ], width=6, className='bg-light'),
        dbc.Col([
            dcc.Graph(id='hist-plot',figure={})
        ], width=6, className='bg-light')
    ])

])

@app.callback(
    Output(component_id='line-plot', component_property='figure'),
    [Input(component_id='bp-1', component_property='n_clicks')],
    [State(component_id='DD-Candidat', component_property='value'),
     State(component_id='kpi-1', component_property='value')],
    prevent_initial_call=True
)
def update_lineplot(n, candidate, kpi):
    df2 = fc.is_candidate_summary(dataframe, candidate, on=kpi)
    if kpi=='number':
        ax = 'Number of Tweets'
        col = 'tweet_id'
    elif kpi=='account':
        ax = 'Number of Accounts'
        col = 'username'
    else:
        ax = 'Number of Likes'
        col = 'n_like'
    figure={}
    figure['data'] = []
    for elt in df2['Candidat'].unique():
        c = df2[df2['Candidat']==elt].reset_index(drop=True)
        figure['data'].append(go.Scatter(x=c['day'], y=c[col], name=elt, mode='lines'))
    figure['layout'] = go.Layout(xaxis={'title':'Date'}, yaxis={'title':ax})
    return figure


@app.callback(
    Output(component_id='hist-plot', component_property='figure'),
    [Input(component_id='bp-2', component_property='n_clicks')],
    [State(component_id='DD-Candidat2', component_property='value')],
    prevent_initial_call=True
)
def update_histplot(n, candidate):
    df2 = fc.account_candidate_hist(dataframe, candidate)
    if candidate == 'All':
        OPACITY = 0.65
    else:
        OPACITY = 1
    figure={}
    figure['data'] = []
    for elt in df2['Candidat'].unique():
        c = df2[df2['Candidat']==elt].reset_index(drop=True)
        figure['data'].append(go.Histogram(x=c['account_history'], opacity=OPACITY, nbinsx=80, name=elt))
    figure['layout'] = go.Layout(title='Distribution of Accounts Ages (Days)',
                                 xaxis={'title':'Age of Accounts in Days'},
                                 yaxis={'title':'Number of Accounts'})
    return figure

@app.callback(
    Output(component_id='title_page', component_property='children'),
    [Input(component_id='url1', component_property='pathname')],
    prevent_initial_call=False
)
def read_data(p_name):
    global dataframe
    dataframe = pd.read_csv('datasets/tweets_prez.csv', encoding='utf-8-sig')
    dataframe = fc.data_processing(dataframe)
    return 'Élection Présidentielle 2022'
