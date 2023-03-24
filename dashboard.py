import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import os
import time

def load_data():
    data = pd.read_csv("data.csv")
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    return data

def daily_report(data):
    data['date'] = data['timestamp'].dt.date
    daily_data = data.groupby('date').agg(
        open_rate=('rate', 'first'),
        close_rate=('rate', 'last'),
        high_rate=('rate', 'max'),
        low_rate=('rate', 'min')
    )
    daily_data['percentage_change'] = (daily_data['close_rate'] - daily_data['open_rate']) / daily_data['open_rate'] * 100
    return daily_data

app = dash.Dash(__name__)

data = load_data()

app.layout = html.Div(
    children=[
        html.H1(children="Taux de change EUR/USD"),
        dcc.DatePickerRange(
            id='date-picker',
            min_date_allowed=data['timestamp'].min().date(),
            max_date_allowed=data['timestamp'].max().date(),
            start_date=data['timestamp'].min().date(),
            end_date=data['timestamp'].max().date()
        ),
        dcc.Graph(id="live-update-graph"),
        dcc.Interval(
            id="interval-component",
            interval=60 * 1000,  # Mise à jour toutes les minutes
            n_intervals=0,
        ),
        html.H2(children="Rapport quotidien"),
        dash_table.DataTable(
            id="daily-report-table",
            columns=[
                {"name": "Date", "id": "date"},
                {"name": "Ouverture", "id": "open_rate"},
                {"name": "Clôture", "id": "close_rate"},
                {"name": "Haut", "id": "high_rate"},
                {"name": "Bas", "id": "low_rate"},
                {"name": "Variation en %", "id": "percentage_change"},
            ],
            style_cell={"textAlign": "center"},
            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
        ),
    ]
)

@app.callback(
    Output("live-update-graph", "figure"),
    Input("interval-component", "n_intervals"),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)

def update_dashboard(n, start_date, end_date):
    data = load_data()
    data = data[(data['timestamp'].dt.date >= pd.to_datetime(start_date)) & (data['timestamp'].dt.date <= pd.to_datetime(end_date))]
    
    trace = go.Scatter(x=data["timestamp"], y=data["rate"], mode="lines+markers", name="Taux de change")

    data["moving_average"] = data["rate"].rolling(window=5).mean()
    moving_average_trace = go.Scatter(x=data["timestamp"], y=data["moving_average"], mode="lines", name="Moyenne mobile")

    data["volatility"] = data["rate"].rolling(window=5).std()
    volatility_trace_upper = go.Scatter(x=data["timestamp"], y=data["moving_average"] + data["volatility"], mode="lines", name="Volatilité supérieure", line={"dash": "dash"})
    volatility_trace_lower = go.Scatter(x=data["timestamp"], y=data["moving_average"] - data["volatility"], mode="lines", name="Volatilité inférieure", line={"dash": "dash"})

    return {
        "data": [trace, moving_average_trace, volatility_trace_upper, volatility_trace_lower],
        "layout": go.Layout(
            xaxis={"title": "Date et heure"},
            yaxis={"title": "Taux de change"},
            showlegend=True,
            margin=dict(l=40, r=0, t=40, b=30),
        ),
    }
@app.callback(
    Output("daily-report-table", "data"),
    Input("interval-component", "n_intervals"),
)
def update_daily_report(n):
    data = load_data()
    daily_data = daily_report(data)
    return daily_data.reset_index().to_dict("records")

if __name__ == "__main__":
    app.run_server(debug=True)
