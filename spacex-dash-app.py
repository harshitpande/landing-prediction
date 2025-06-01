# Import required libraries
import pandas as pd
import dash
from dash import Dash, html, dcc
# import dash_html_components as html
# import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()
                                    ] + [{'label': 'All Sites', 'value': 'ALL'}],
                                    value='ALL',
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                ),       
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    value=[min_payload, max_payload]
                                ),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# Callback for Pie Chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, 
                     names='Launch Site', 
                     title='Total Success Launches By Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, 
                     names='class', 
                     title=f'Total Success Launches for {entered_site}')
    return fig

# Callback for Scatter Plot
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), 
     Input('payload-slider', 'value')]
)
def get_scatter_plot(entered_site, slider_range):
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= slider_range[0]) & 
        (spacex_df['Payload Mass (kg)'] <= slider_range[1])
    ]
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
    
    fig = px.scatter(
        data_frame=filtered_df,
        x='Payload Mass (kg)', 
        y='class', 
        color='Booster Version Category',
        title='Correlation between Payload and Success for All Sites' if entered_site == 'ALL' else f'Correlation for {entered_site}'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

