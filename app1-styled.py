# Team 9 - MSBA Session 2
# Vanessa Broadrup, Luke Kovats, Suyog Mainali, Bryce Marin

# Question/Story: What are you trying to show and why?
# In CTBA class, we have recently been examining the relationships between business and AI–as well as how advancements in AI affect business and business operations. For this assignment, we wanted to take advantage of the opportunity to look at financial data in order to investigate how a company like NVIDIA, which has demonstrated substantial growth in the AI sphere, performs in the stock market over a period of three years. NVDA has been a very volatile stock over the past 3 years. By examining the relationships between stock price and volatility, we aim to get an idea of the risk of owning NVDA over time.

# Data Choices: Which tickers/series and time span, and why?
# On the y axis on the left side, we measured stock price. On the right, we measured percent volatility, and on the x axis, we took note of January and July of each year from 2023-2025. On the dash, a user can hover over the graph for more specific date information.

# Takeaway (2–3 sentences): What should a reader notice?
# The reader should notice that when there is a sudden uptick in price on the graph, there tends to also be a sudden increase in volatility. When prices tend to stabilize, volatility tends to go down. 

# Sources
# https://python-graph-gallery.com/line-chart-dual-y-axis-with-matplotlib/
# https://www.reddit.com/r/econometrics/comments/12zh95u/calculate_30days_volatility_using_python/
# https://www.youtube.com/watch?v=nfJ1Ou0vonE
# AI was used to help edit axis 

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import yfinance as yf
import plotly.graph_objects as go
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url

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
    name="Price ($)"
))

# Volatility line (right y-axis)
fig.add_trace(go.Scatter(
    x=df.index, y=df["Volatility30"],
    name="30 Day Volatility (%)",
    line=dict(dash="dash"),
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
    ),
    yaxis2=dict(
        title="30 Day Volatility (%)",
        overlaying="y",
        side="right",
    ),
    legend=dict(x=0.01, y=0.99, bordercolor="lightgray", borderwidth=1)
)

app = dash.Dash(__name__)
# adds the theme changer button
theme_change = ThemeChangerAIO(aio_id="theme")
app.title = "Group 9 Dash"

app.layout = dbc.Container([
    theme_change,
    # row for the header of title and people
    dbc.Row([
        dbc.Col(html.Div(html.H2("Analyzing NVDA Stock"))),
        dbc.Col(html.Div(dbc.Alert("Vanessa Broadrup, Luke Kovats, Suyog Mainali, Bryce Marin", color="secondary")),
                width={"size": 8})
    ]),
    dbc.Row([
        # information column
        dbc.Col([
            # card for year range
            dbc.Card([
                dbc.CardHeader("Date Range:"),
                dbc.CardBody([
                    html.P([
                        f"NVDA Stock from:", html.Br(), f"{start_date} → {end_date}"],
                        className="card-text",
                    ),
                ])
            ]),
            # card for analysis
            dbc.Card([
                dbc.CardHeader("Graph Analysis:"),
                dbc.CardBody([
                    html.P(
                        "We are investigating how a volatile stock company like NVIDIA, which has demonstrated substantial growth in the AI sphere, performs in the stock market over a period of three years. The reader should notice that when there is a sudden uptick in price on the graph, there tends to also be a sudden increase in volatility. When prices tend to stabilize, volatility tends to go down.",
                        className="card-text",
                    ),
                ])
            ])
        ], style={"margin-top":"35px"}),
        # column for graph
        dbc.Col([
            html.Div(dcc.Graph(id="main-graph", figure=fig)),
            html.Div(html.P("Source: Yahoo Finance (yfinance)", 
                       style={"fontSize": "12px",
                              "color": "gray",
                              "marginTop": "10px",
                              "textAlign": "center",
                              "fontStyle": "italic"})),
        ], width={"size": 8}),
    ])
], fluid=True, style={"margin-top":"10px"})

# getting callback for theme switch
@app.callback(
    Output("main-graph", "figure"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)

# updating the graph when theme is switched
def update_graph_theme(theme):
    template=template_from_url(theme)
    fig = go.Figure(layout=go.Layout(template=template))
    # Price line (left y-axis)
    fig.add_trace(go.Scatter(
        x=df.index, y=df["Close"],
        name="Price ($)"
    ))
    # Volatility line (right y-axis)
    fig.add_trace(go.Scatter(
        x=df.index, y=df["Volatility30"],
        name="30 Day Volatility (%)",
        line=dict(dash="dash"),
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
        ),
        yaxis2=dict(
            title="30 Day Volatility (%)",
            overlaying="y",
            side="right",
        ),
        legend=dict(x=0.01, y=0.99, bordercolor="gray", borderwidth=1)
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=False)
