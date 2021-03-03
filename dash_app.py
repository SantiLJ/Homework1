#Santiago Le Jeune ; santiago.le.jeune@duke.edu ; 02/25/2021

import dash                                             #imports
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import pandas as pd
from os import listdir, remove
import pickle
from time import sleep
from helper_functions import * # this statement imports all functions from your helper_functions file!

# Run helper function to clear out any io files left over
check_for_and_del_io_files()

app = dash.Dash(__name__)           #Dash App

# Dash App layout

app.layout = html.Div([

    # Section title
    html.H1("Section 1: Fetch & Display exchange rate historical data"),

    # Currency pair text input, within its own div.
    html.Div(
        [
            "Input Currency: ",
            html.Div(dcc.Input(id = 'currency-pair', value = "AUDCAD",type = 'text'))
        ],
        style={'display': 'inline-block'})
    ,
    # Submit button:
        html.Button('Submit', id = 'submit-button', n_clicks = 0)
    ,
    # Line break
        html.Br()
    ,
    # Div to hold the initial instructions and the updated info once submit is pressed
        html.Div(id='output-div', children='Enter a currency code and press submit')
    ,
    html.Div([
        # Candlestick graph goes here:
        dcc.Graph(id='candlestick-graph')
    ]),
    # Another line break
        html.Br()
    ,
    # Section title
        html.H1("Section 2: Make a Trade")
    ,
    # Div to confirm what trade was made
        html.Div(id='trade-output')
    ,
    # Radio items to select buy or sell
    dcc.RadioItems(
            id='action',options=
            [
                {'label': 'BUY', 'value': 'BUY'},
                {'label': 'SELL', 'value': 'SELL'},
            ]
            ,
            value='BUY')
    ,
    # Text input for the currency pair to be traded
        html.Div(
            ["Trade Currency:",
             html.Div(dcc.Input(id = 'trade_currency',value = "AUDCAD" , type = 'text'))
             ],
             style={'display': 'inline-block'})
    ,
    # Numeric input for the trade amount
        html.Div(
            [
                "Trade Amount:",
                html.Div(dcc.Input(id = 'trade_amt', value = '1000',type = 'number'))
            ],
             style={'display': 'inline-block'})
    ,
    # Submit button for the trade
    html.Button('Trade', id = 'trade-button', n_clicks = 0)

])

# Callback for what to do when submit-button is pressed
@app.callback(
    [ # Use an array as output for the multiple outputs
    Output('output-div', 'children'),
    Output('candlestick-graph', 'figure')
    ],
    Input('submit-button', 'n_clicks'),
    State('currency-pair', 'value')
)

def update_candlestick_graph(n_clicks, value):
    # n_clicks doesn't get used, we only include it for the dependency.
    #Output text for ccy pair output, candlestick figure

    # Save the value of currency-input as a text file.
    text_file = open("currency_pair.txt", 'w')
    text_file.write(value)
    text_file.close()

    # Wait until ibkr_app runs the query and saves the historical prices csv
    while not 'currency_pair_history.csv' in listdir():        #using a set as it is more efficient
        sleep(0.01)

    # Read in the historical prices
    df =pd.read_csv('currency_pair_history.csv')
    # Remove the file 'currency_pair_history.csv'
    remove('currency_pair_history.csv')
    # Make the candlestick figure

    fig = go.Figure(
        data=[
            go.Candlestick(
                x   =   df['date'],
                open=   df['open'],
                high=   df['high'],
                low =   df['low'],
                close=  df['close']
            )
        ],
    )
    fig.update_layout(title='{} History'.format(value))

    # Return updated text to currency-output, and the figure to candlestick-graph outputs
    return ('Submitted query for ' + value), fig

# Callback for what to do when trade-button is pressed
@app.callback(
    Output('trade-output', 'children'),
    Input('trade-button', 'n_clicks'),
    Input('action', 'value'),
    State('trade_currency', 'value'),
    State('trade_amt', 'value'),
    prevent_initial_call=True
)

def trade(n_clicks, action, trade_currency, trade_amt):
    # Still don't use n_clicks, but we need the dependency
    # Message that we want to send back to trade-output
    msg = '{} {} {}'.format(action, trade_currency, trade_amt)

    # Make our trade_order object -- a DICTIONARY.
    trade_order = {"action":action, "trade_currency":trade_currency, "trade_amt":trade_amt}

    # Dump trade_order as a pickle object to a file connection opened with write-in-binary ("wb") permission:
    pickle.dump(trade_order, open("trade_order.p", 'wb'))

    # Return the message, which goes to the trade-output div's "children" attribute.
    return msg

# Run it!
if __name__ == '__main__':
    app.run_server(debug=True)
