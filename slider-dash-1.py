import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import os

# Load dataset
file_path = "data.csv"
df = pd.read_csv(file_path)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

# Compute Central Moving Average (CMA)
def central_moving_average(data, window):
    return data.rolling(window=window, center=True).mean()

# Create Dash app
app = dash.Dash(__name__)

# app.layout = html.Div([
#     html.H1("Dynamic CMA Plot", style={'textAlign': 'center'}),
    
#     # Slider with continuous update while dragging
#     dcc.Slider(
#         id='window-slider',
#         min=1, max=201, step=2, value=1,
#         marks={i: str(i) for i in range(1, 200, 20)},
#         tooltip={"placement": "bottom", "always_visible": True},
#         updatemode="drag",  # Ensures real-time updates

#     ),
    
#     # Graph for the moving average
#     dcc.Graph(id='cma-plot', config={'displayModeBar': False}),
# ])

app.layout = html.Div([
    html.H1("Dynamic CMA Plot", style={'textAlign': 'center'}),

    # Slider container with min/max labels
    html.Div([
        dcc.Slider(
            id='window-slider',
            min=1, max=201, step=2, value=1,
            marks={i: str(i) for i in range(1, 202, 200)},
            tooltip={"placement": "bottom", "always_visible": False},
            updatemode="drag",  # Ensures real-time updates
        ),
        
        # Min/Max labels
        html.Div([
            html.Span("Min Smoothing", style={"float": "left", "font-weight": "bold"}),
            html.Span("Max Smoothing", style={"float": "right", "font-weight": "bold"})
        ], style={"margin-top": "-5px"})  # Adjust positioning
    ], style={"width": "60%", "margin": "20px"}),  # Center align

    # Graph for the moving average
    dcc.Graph(id='cma-plot', config={'displayModeBar': False}),
])


@app.callback(
    Output('cma-plot', 'figure'),
    Input('window-slider', 'value')
)
def update_plot(k):
    df['CMA'] = central_moving_average(df['value'], k)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'][100:-100], 
                             y=df['CMA'][100:-100], 
                             mode='lines',
                             name=f'CMA (k={k})',
                             line=dict(color='blue')))

    fig.update_layout(
        xaxis=dict(range=[df['date'].iloc[100], df['date'].iloc[-100]]),
        yaxis=dict(range=[40, 48]),
        title="Central Moving Average (CMA) with Adjustable Window Size",
        xaxis_title="Date",
        yaxis_title="Value",
        template="plotly_white"
    )
    return fig

# Run the app
import os
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))  # Get port from Render, default to 8050
    app.run_server(host='0.0.0.0', port=port)
    







