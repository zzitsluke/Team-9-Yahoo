import dash
from dash import dcc, html
import yfinance as yf
import plotly.graph_objects as go

# Fetch NVDA data
nvda = yf.Ticker("NVDA")
df = nvda.history(period="3y")

# Compute 30-day volatility
df["percent_change"] = df["Close"].pct_change()
df["Volatility30"] = df["percent_change"].rolling(30).std() * 100

# Get start and end date for display
start_date = df.index.min().strftime("%Y-%m-%d")
end_date = df.index.max().strftime("%Y-%m-%d")

# Create Plotly figure with two y-axes
fig = go.Figure()

# Price line (left y-axis)
fig.add_trace(go.Scatter(
    x=df.index, y=df["Close"],
    name="Price ($)", line=dict(color="#3399e6")
))

# Volatility line (right y-axis)
fig.add_trace(go.Scatter(
    x=df.index, y=df["Volatility30"],
    name="30 Day Volatility (%)",
    line=dict(color="#FF0000", dash="dash"),
    yaxis="y2"
))

# Layout with dual y-axis
fig.update_layout(
    title="3 Year Price vs Volatility for NVDA",
    xaxis=dict(
        tickformat="%b %Y",
        tickangle=45
    ),
    yaxis=dict(
        title="Price ($)",
        color="#3399e6"
    ),
    yaxis2=dict(
        title="30 Day Volatility (%)",
        overlaying="y",
        side="right",
        color="#FF0000"
    ),
    legend=dict(x=0.01, y=0.99, bordercolor="gray", borderwidth=1)
)

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div(id="main-container", children=[

    # Title
    html.Div(id="title-div", children=[
        html.H1("Dashboard Title")
    ]),

    # Content row
    html.Div(id="content-div", style={"display": "flex"}, children=[

        # Sidebar
        html.Div(id="sidebar-div", style={"flex": "1"}, children=[
            html.Div(id="year-div", children=[
                html.Label(f"Date Range: {start_date} → {end_date}")
            ]),
            html.Div(id="analysis-div", children=[
                html.Label("Graph Analysis (to be written later)")
            ])
        ]),

        # Graph
        html.Div(id="graph-div", style={"flex": "3"}, children=[
            dcc.Graph(id="main-graph", figure=fig)
        ])
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)