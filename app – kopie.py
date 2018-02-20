import dash; from dash.dependencies import Input, Output
import dash_core_components as dcc; import dash_html_components as html
import pandas as pd; import plotly.graph_objs as go
from datetime import datetime

app = dash.Dash()

# layout
app.layout = html.Div(style={'padding-top': '20px', 'padding-bottom': '50px', 'padding-left': '70px', 'padding-right': '70px', 'backgroundColor': '#f4f4f4', 'font-family': 'sans-serif'},
children=[
    html.H1(children='New York Air Quality Data: Interactive Diagram', style={'text-shadow': '3px 3px #ffffff'}),
    html.Div([
        html.P('Navigate through data pertaining to ozone layer measurements, amounts of solar radiation, wind velocity & temperature.'),
        html.P('Select data type and plot type:')
    ], style={'color': '#000444', 'fontSize': 16, 'font-weight': 'bold'}),
    dcc.Dropdown(
        options=[
            {'label': 'Ozone layer thickness', 'value': 'Ozone'},
            {'label': 'Solar radiation', 'value': 'Solar.R'},
            {'label': 'Wind velocity', 'value': 'Wind'},
            {'label': 'Temperature', 'value': 'Temp'}],
        value='Temp',
        id = 'dropdown_input'
    ),
    html.Br(),
    dcc.RadioItems(
        options=[
            {'label': 'Scatter graph: day-by-day', 'value': 'scatter'},
            {'label': 'Boxplot: month-by-month', 'value': 'box'}],
        value='scatter',
        id='radio_input'
    ),
    html.Br(),
    dcc.Graph(id='newyork_graph')
])

# callback
@app.callback(
    Output(component_id='newyork_graph', component_property='figure'),
    [Input(component_id='radio_input', component_property='value'),
    Input(component_id='dropdown_input', component_property='value')]
)

def update_figure(plot_type, data_type):
    if plot_type == 'scatter':
        trace = go.Scatter(
                x = dataset.Date,
                y = dataset[data_type],
                mode = 'lines', name = data_type)
        data = [trace]
    elif plot_type == 'box':
        trace1 = go.Box(y = dataset[data_type].loc[(dataset.Month == 5)], name = 'May', boxpoints = 'outliers')
        trace2 = go.Box(y = dataset[data_type].loc[(dataset.Month == 6)], name = 'Jun', boxpoints = 'outliers')
        trace3 = go.Box(y = dataset[data_type].loc[(dataset.Month == 7)], name = 'Jul', boxpoints = 'outliers')
        trace4 = go.Box(y = dataset[data_type].loc[(dataset.Month == 8)], name = 'Aug', boxpoints = 'outliers')
        trace5 = go.Box(y = dataset[data_type].loc[(dataset.Month == 9)], name = 'Sep', boxpoints = 'outliers')

        data = [trace1, trace2, trace3, trace4, trace5]

    figure = {
        'data': data,
        'layout': {
            'title': 'New York Air Quality Data',
            'showlegend': False,
            'yaxis': {'title': data_type}
        }
    }
    return figure

# get clean data from dataset
dataset = pd.read_csv('https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/datasets/airquality.csv')
dataset = dataset.drop('Unnamed: 0', 1)
dataset['Year'] = 2017
dataset['Date'] = pd.to_datetime(dataset.Year*10000+dataset.Month*100+dataset.Day,format='%Y%m%d')
for i in ['Day', 'Year']:
    del dataset[i]

# run
if __name__ == '__main__':
    app.run_server()