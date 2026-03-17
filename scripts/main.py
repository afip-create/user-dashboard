import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

# Create a Dash application
app = dash.Dash(__name__)

# Define a layout for the application
app.layout = html.Div([
    html.H1('User Dashboard'),
    dcc.Graph(id='graph'),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Option 1', 'value': 'option1'},
            {'label': 'Option 2', 'value': 'option2'},
            {'label': 'Option 3', 'value': 'option3'}
        ],
        value='option1'
    )
])

# Define a callback function for the dropdown
@app.callback(
    Output('graph', 'figure'),
    [Input('dropdown', 'value')]
)
def update_graph(selected_value):
    # Simulate a DataFrame for demonstration purposes
    df = pd.DataFrame({
        'x': [1, 2, 3],
        'y': [4, 5, 6]
    })

    # Filter the DataFrame based on the selected dropdown value
    if selected_value == 'option1':
        filtered_df = df[df['x'] > 1]
    elif selected_value == 'option2':
        filtered_df = df[df['x'] < 2]
    else:
        filtered_df = df

    # Create a line chart with the filtered data
    fig = {
        'data': [
            {'x': filtered_df['x'], 'y': filtered_df['y'], 'type': 'line'}
        ],
        'layout': {
            'title': 'Line Chart',
            'xaxis': {'title': 'X Axis'},
            'yaxis': {'title': 'Y Axis'}
        }
    }

    return fig

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)