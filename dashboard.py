import dash
from dash import dcc, html
import plotly.graph_objs as go
import time

# Create the Dash app
app = dash.Dash(__name__)

# Data for the graph (prices will be updated every minute)
price_data = []
timestamps = []

# Function to read the current price from the price.txt file
def read_price():
    with open('price.txt', 'r') as f:
        return f.read().strip()

# Layout of the app with custom styles
app.layout = html.Div(
    children=[
        # Title of the dashboard
        html.H1("USD/JPY Price Tracker", style={'textAlign': 'center', 'color': '#0D47A1', 'fontSize': '50px'}),
       
        # Display the current USD/JPY price
        html.Div(id='live-update-price', style={'textAlign': 'center', 'fontSize': '24px', 'color': 'gray'}),
       
        # Graph of USD/JPY price over time
        dcc.Graph(id='live-update-graph'),
       
        # Update every minute
        dcc.Interval(
            id='interval-component',
            interval=1*60*1000,  # Update every minute
            n_intervals=0
        ),
    ],
    style={'backgroundColor': '#f0f4f8', 'padding': '20px'}  # Background color of the page
)

# Callback to update the current price
@app.callback(
    dash.dependencies.Output('live-update-price', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_price(n):
    price = read_price()  # Read the price from the file
    return f"Current USD/JPY Price: {price}"

# Callback to update the price graph
@app.callback(
    dash.dependencies.Output('live-update-graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    price = read_price()  # Read the price from the file
    timestamps.append(time.strftime("%H:%M:%S"))
    price_data.append(float(price))  # Add the new price to the price data
    return {
        'data': [go.Scatter(x=timestamps, y=price_data, mode='lines+markers', line=dict(color='yellow'))],
        'layout': go.Layout(
            title='USD/JPY Price over Time',
            xaxis=dict(title='Time', showgrid=False),
            yaxis=dict(title='Price', showgrid=True),
            hovermode='closest',
            plot_bgcolor='#1c1c1c',  # Background color of the graph
            paper_bgcolor='#1c1c1c',  # Background color of the page
            font=dict(family='Arial, sans-serif', size=14, color='gray')  # Text in gray
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)
