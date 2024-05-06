import dash
from dash import dcc, html, Input, Output, State
import requests

app = dash.Dash(__name__)

# Define colors
colors = {
    'orange': '#FFA500',
    'white': '#FFFFFF',
    'black': '#000000',
    'brown': '#8B4513'
}

# Define the layout of the dashboard with color styling
app.layout = html.Div(style={'backgroundColor': colors['brown'], 'color': colors['white']}, children=[
    # Header
    html.H1("Suricata Dashboard", style={'textAlign': 'center'}),
    
    # Agent Overview Section
    html.Div(style={'backgroundColor': colors['orange'], 'padding': '10px'}, children=[
        html.H2("Agent Overview"),
        # Display total number of agents
        html.Div(id='total-agents', style={'color': colors['white']}),
        # Show a summary of agents' status
        html.Div(id='agent-status-summary', style={'color': colors['white']})
    ]),
    
    # Detailed Information Section
    html.Div(style={'backgroundColor': colors['orange'], 'padding': '10px'}, children=[
        html.H2("Detailed Information"),
        # Placeholder for detailed information about the selected agent
        html.Div(id='detailed-info', style={'color': colors['white']})
    ]),
    
    # Command-Line Interface Section
    html.Div(style={'backgroundColor': colors['black'], 'padding': '10px'}, children=[
        html.H2("Command-Line Interface", style={'color': colors['white']}),
        # Placeholder for the command-line interface
        html.Div([
            html.Span("$ ", style={'color': colors['orange'], 'font-weight': 'bold'}),
            dcc.Input(id='command-input', type='text', placeholder='Enter command...', style={'width': '70%', 'color': colors['white'], 'backgroundColor': colors['black'], 'border': 'none', 'outline': 'none'}),
            html.Button('Submit', id='submit-button', n_clicks=0, style={'margin-left': '10px', 'backgroundColor': colors['black'], 'color': colors['white'], 'border': '1px solid ' + colors['orange'], 'cursor': 'pointer'})
        ])
    ]),
    
    # Notification Section
    html.Div(id='notification'),
    
    # ELK Stack Button
    html.Div(style={'textAlign': 'center', 'padding': '20px'}, children=[
        html.A(html.Button('View PCAP Data in ELK', id='elk-button', n_clicks=0, style={'backgroundColor': colors['orange'], 'color': colors['white'], 'border': 'none', 'padding': '10px 20px', 'fontSize': '16px', 'cursor': 'pointer'}), href='http://127.0.0.1:5601', target='_blank')
    ])
])

# Function to send command to the Flask server and receive result
def send_command_to_server(command):
    try:
        response = requests.post('http://your_server_ip:5000/execute-command', json={'command': command})
        if response.status_code == 200:
            return response.json()['result']
        else:
            return f"Error: Server returned status code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

# Callback to handle command submission and display output
@app.callback(
    Output('notification', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('command-input', 'value')]
)
def execute_command(n_clicks, command):
    if n_clicks > 0:
        if command:
            result = send_command_to_server(command)
            return html.Div(result, style={'color': colors['white']})
        else:
            return html.Div("No command entered", style={'color': colors['white']})
    else:
        return dash.no_update

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8050, debug=True)
