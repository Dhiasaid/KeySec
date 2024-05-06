import requests

# Define the URL of your Django API endpoint
api_url = 'http://127.0.0.1:8000/api/data/'

# Make a GET request to the API endpoint
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract data from the response JSON
    data = response.json()
    # Process the data and render it in your dashboard
    render_dashboard(data)
else:
    # Handle errors
    print('Error:', response.status_code)
