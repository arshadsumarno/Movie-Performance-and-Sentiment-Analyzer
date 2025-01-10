import os
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline
import dash_bootstrap_components as dbc

# --------------------
# HELPER FUNCTION FOR SMOOTHING
# --------------------
def smooth_line(x, y, points=300):
    valid_data = pd.notna(y)  # Ensure no NaN values
    x, y = x[valid_data], y[valid_data]
    if len(x) >= 3:  # Interpolation requires at least 3 points
        spline = make_interp_spline(x, y)
        x_smooth = np.linspace(x.min(), x.max(), points)
        y_smooth = spline(x_smooth)
        return pd.to_datetime(x_smooth), y_smooth
    return x, y  # Return original if smoothing is not possible

# --------------------
# LOAD FRANCHISE CSVs
# --------------------
csv_folder = "csvs"
franchise_csvs = [file for file in os.listdir(csv_folder) if file.endswith("_movies.csv")]

# Create a dictionary of franchises with display names
franchises = {
    csv.replace("_movies.csv", "").replace("_", " "): os.path.join(csv_folder, csv)
    for csv in franchise_csvs
}

# --------------------
# DASH APP SETUP
# --------------------
app = dash.Dash(external_stylesheets=[dbc.themes.LUMEN])

app.layout = html.Div([
    html.H1("Performance and Sentiment Analyzer: Movie Franchises"),
    html.Div([
        dcc.Dropdown(
            id='franchise-dropdown',
            options=[{'label': name.title(), 'value': path} for name, path in franchises.items()],
            value=list(franchises.values())[0],  
            placeholder="Select a Movie Franchise"
        )
    ]),
    html.Div([
        dcc.Graph(id='time-series-graph'),
        html.Div(id='hover-data-box')
    ], style={'display': 'flex', 'flex-direction': 'row'})
])

# --------------------
# CALLBACK FOR UPDATING GRAPH
# --------------------
@app.callback(
    Output('time-series-graph', 'figure'),
    Input('franchise-dropdown', 'value')
)
def update_graph(selected_csv):
    # Load the selected franchise data
    df = pd.read_csv(selected_csv)

    # Convert release_date to datetime
    df['release_date'] = pd.to_datetime(df['release_date'], format="%b %d, %Y", errors='coerce')
    df = df.sort_values(by='release_date')

    # Ensure sentiment_score is numeric
    df['sentiment_score'] = pd.to_numeric(df['sentiment_score'], errors='coerce')

    # Add a formatted release date column for display purposes
    df['formatted_release_date'] = df['release_date'].dt.strftime('%b %d, %Y')

    # Smooth performance and sentiment lines
    x_numeric = pd.to_numeric(df['release_date'])
    x_smooth_perf, y_smooth_perf = smooth_line(x_numeric, df['performance'])
    x_smooth_sent, y_smooth_sent = smooth_line(x_numeric, df['sentiment_score'])

    # Create the figure
    fig = go.Figure()

    # Smoothed performance line
    fig.add_trace(go.Scatter(
        x=x_smooth_perf,
        y=y_smooth_perf,
        mode='lines',
        name='Performance',
        line=dict(color='#e63946', width=2),
        hoverinfo='skip',
        showlegend=False,
        legendgroup='Performance'
    ))

    # Add original points with detailed hover info
    fig.add_trace(go.Scatter(
        x=df['release_date'],
        y=df['performance'],
        mode='markers',
        marker=dict(size=4, color='#e63946'),
        name='Performance',
        customdata=df[['title', 'formatted_release_date', 'production_budget', 'box_office', 'profit', 
                        'roi_percentage', 'performance', 'poster_url', 'backdrop_url', 'runtime', 
                        'tagline', 'trailer', 'sentiment_score', 'comment']].values,
        hovertemplate=None,
        legendgroup='Performance'
    ))

    # Smoothed sentiment line
    fig.add_trace(go.Scatter(
        x=x_smooth_sent,
        y=y_smooth_sent,
        mode='lines',
        name='Sentiment',
        line=dict(color='#457b9d', width=2),
        hoverinfo='skip',
        showlegend=False,
        legendgroup='Sentiment'
    ))

    # Original sentiment points
    fig.add_trace(go.Scatter(
        x=df['release_date'],
        y=df['sentiment_score'],
        mode='markers',
        marker=dict(size=4, color='#457b9d'),
        name='Sentiment',
        customdata=df[['title', 'formatted_release_date', 'production_budget', 'box_office', 'profit', 
                        'roi_percentage', 'performance', 'poster_url', 'backdrop_url', 'runtime', 
                        'tagline', 'trailer', 'sentiment_score', 'comment']].values,
        hovertemplate=None,
        legendgroup='Sentiment'
    ))

    fig.update_layout(
        title='Performance and Sentiment Over Time',
        xaxis_title='Release Date',
        yaxis_title='Performance/Sentiment',
        hovermode='x unified',
    )

    return fig

# --------------------
# CALLBACK FOR HOVER DATA
# --------------------
@app.callback(
    Output('hover-data-box', 'children'),
    Input('time-series-graph', 'hoverData'),
    Input('franchise-dropdown', 'value')
)
def display_hover_data(hover_data, selected_csv):
    if hover_data is None:
        return html.Div([
            html.Div([
                html.H3("Hover Over the Graph For More Information"),
                html.P("...", id='release-date'),
            ], id='movie-text'),
            html.Div([
                html.Div([
                    html.Img(src='https://placehold.co/2000x3000?text=...'),
                    html.Img(src='https://placehold.co/410x280?text=...'),
                ], id='image-container')
            ]),
            html.Div([
                html.Div([
                    html.Img(src='./assets/movie.png', alt='Icon by juicy_fish', id='icon'),
                    html.Div([
                        html.P("-.--", id='metric-text-value'),
                        html.B("Performance", id='metric-text'),
                    ], id='metric-text-container'),
                ], id='metric-container'),
                html.Div([
                    html.Img(src='./assets/ticket.png', alt='Icon by juicy_fish', id='icon'),
                    html.Div([
                        html.P("-.--", id='metric-text-value'),
                        html.B("Sentiment", id='metric-text'),
                    ], id='metric-text-container'),
                ], id='metric-container'),
            ], id='score-container'),
            html.Div([
                html.Div([
                    html.Div([
                        html.P(f"Production Budget: "),
                        html.P(f"Box Office: "),
                    ], id='stats-container-half'),
                    html.Div([
                        html.P(f"Profit: "),
                        html.P(f"ROI Percentage: "),
                    ], id='stats-container-half'),
                ], id='stats-container'),
                html.Div([
                    html.P([
                        "Comment: ",
                    ])
                ], id='comment-container')
            ], id='stats'),
        ])
    
    # Extract data for the hovered point
    point_data = hover_data['points'][0]['customdata']
    poster_url = point_data[7]  # Extract poster URL
    backdrop_url = point_data[8]
    trailer = point_data[11]

    return html.Div([
        html.Div([
            html.H3(f"{point_data[0]}"),
            html.P(f"{point_data[1]} · {point_data[9]} min · {point_data[10]}", id='release-date'),
        ], id='movie-text'),
        html.Div([
            html.Div([
                html.Img(src=poster_url),
                html.Iframe(src=trailer),
            ], id='image-container')
        ]),
        html.Div([
            html.Div([
                html.Img(src='./assets/movie.png', alt='Icon by juicy_fish', id='icon'),
                html.Div([
                    html.P(f"{point_data[6]}", id='metric-text-value'),
                    html.B("Performance", id='metric-text'),
                ], id='metric-text-container'),
            ], id='metric-container'),
            html.Div([
                html.Img(src='./assets/ticket.png', alt='Icon by juicy_fish', id='icon'),
                html.Div([
                    html.P(f"{point_data[12]}", id='metric-text-value'),
                    html.B("Sentiment", id='metric-text'),
                ], id='metric-text-container'),
            ], id='metric-container'),
        ], id='score-container'),
        html.Div([
            html.Div([
                html.Div([
                    html.P(f"Production Budget: {point_data[2]}"),
                    html.P(f"Box Office: {point_data[3]}"),
                ], id='stats-container-half'),
                html.Div([
                    html.P(f"Profit: {point_data[4]}"),
                    html.P(f"ROI Percentage: {point_data[5]}"),
                ], id='stats-container-half'),
            ], id='stats-container'),
            html.Div([
                html.P([
                    "Comment: ",
                    html.I(f"{point_data[13]}", style={'color': '#306899'})
                ])
            ], id='comment-container')
        ], id='stats'),
    ])


# --------------------
# RUN THE APP
# --------------------
if __name__ == "__main__":
    app.run_server(debug=True)
