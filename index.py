from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc
# Connect to main app.py file
from app import app
from app import server
import pandas as pd
import functions as fc


# Connect to your app pages

from apps import general_view, second_view, home



app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([dcc.Link('Home', href='/apps/Home')], width=1, className='bg-light'),
        dbc.Col([dcc.Link('Page 1', href='/apps/1')], width=1, className='bg-light'),
        dbc.Col([dcc.Link('Page 2', href='/apps/2')], width=1, className='bg-light')
    ]),
    dbc.Row([
        dcc.Location(id='url', refresh=False)
    ]),
    dbc.Row([
        dbc.Button(id='refresh-button',
                   children=[html.I(className="fa fa-refresh m-1"), "Refresh"],
                   color="info",
                   className="align-middle mt-1"),
        html.Div(id='hidden-refresh', children='')
    ]),
    dbc.Row(id='page-content', children=[])
])

@app.callback(Output(component_id='hidden-refresh', component_property='children'),
              [Input(component_id='refresh-button', component_property='n_clicks')],
              prevent_initial_call=True)
def update_dataframe(n):
    info_str = fc.update_data(fc.dataframe['day'].max(),
                              fc.dataframe[fc.dataframe['day']==fc.dataframe['day'].max()]['tweet_id'])
    fc.dataframe = pd.read_csv('datasets/tweets_prez.csv', encoding='utf-8-sig')
    fc.dataframe = fc.data_processing(fc.dataframe)
    return info_str




@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/1':
        return general_view.layout
    if pathname == '/apps/2':
        return second_view.layout
    else:
        return home.layout


if __name__ == '__main__':
    app.run_server(debug=False)
